from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from db.database import get_db
from db.models import Part, ProductionOrder, Vendor, PurchaseItem
from api.routers.plm import part_to_dict

router = APIRouter()
query_router = APIRouter()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def order_to_dict(o: ProductionOrder) -> dict[str, Any]:
    return {
        "order_id": o.order_id,
        "part_id": o.part_id,
        "production_type": o.production_type,
        "vendor_id": o.vendor_id,
        "quantity": o.quantity,
        "unit_cost_jpy": o.unit_cost_jpy,
        "lead_time_days": o.lead_time_days,
        "delivery_date": str(o.delivery_date),
        "quality_result": o.quality_result,
        "notes": o.notes,
    }


def vendor_to_dict(v: Vendor) -> dict[str, Any]:
    return {
        "vendor_id": v.vendor_id,
        "vendor_name": v.vendor_name,
        "specialty": v.specialty,
        "country": v.country,
        "rating": v.rating,
        "typical_lead_time_days": v.typical_lead_time_days,
    }


def purchase_item_to_dict(pi: PurchaseItem) -> dict[str, Any]:
    return {
        "item_id": pi.item_id,
        "part_id": pi.part_id,
        "vendor_id": pi.vendor_id,
        "catalog_price_jpy": pi.catalog_price_jpy,
        "min_order_qty": pi.min_order_qty,
        "lead_time_days": pi.lead_time_days,
    }


def _require_part(part_id: str, db: Session) -> Part:
    part = db.get(Part, part_id)
    if not part:
        raise HTTPException(status_code=404, detail=f"Part '{part_id}' not found")
    return part


def _cost_summary(orders: list[ProductionOrder]) -> dict[str, Any]:
    by_type: dict[str, list[float]] = {}
    for o in orders:
        by_type.setdefault(o.production_type, []).append(o.unit_cost_jpy)
    summary = {}
    for ptype, costs in by_type.items():
        summary[ptype] = {
            "avg_unit_cost_jpy": round(sum(costs) / len(costs), 2),
            "min_unit_cost_jpy": min(costs),
            "max_unit_cost_jpy": max(costs),
            "order_count": len(costs),
        }
    return summary


def _recommendation(orders: list[ProductionOrder], db: Session) -> dict[str, Any]:
    if not orders:
        return {}

    # Build per-vendor/type aggregates
    buckets: dict[tuple, dict] = {}
    for o in orders:
        key = (o.vendor_id, o.production_type)
        if key not in buckets:
            buckets[key] = {"costs": [], "leads": [], "results": [], "vendor_id": o.vendor_id,
                            "production_type": o.production_type}
        buckets[key]["costs"].append(o.unit_cost_jpy)
        buckets[key]["leads"].append(o.lead_time_days)
        buckets[key]["results"].append(o.quality_result)

    scored = []
    for key, b in buckets.items():
        pass_rate = b["results"].count("pass") / len(b["results"])
        scored.append({
            "vendor_id": b["vendor_id"],
            "production_type": b["production_type"],
            "avg_cost_jpy": round(sum(b["costs"]) / len(b["costs"]), 2),
            "avg_lead_days": round(sum(b["leads"]) / len(b["leads"]), 1),
            "pass_rate": round(pass_rate, 3),
            "sample_count": len(b["costs"]),
        })

    cheapest = min(scored, key=lambda x: x["avg_cost_jpy"])
    fastest = min(scored, key=lambda x: x["avg_lead_days"])
    best_quality = max(scored, key=lambda x: (x["pass_rate"], -x["avg_cost_jpy"]))

    def enrich(rec: dict) -> dict:
        v = db.get(Vendor, rec["vendor_id"]) if rec["vendor_id"] else None
        return {**rec, "vendor_name": v.vendor_name if v else "In-house"}

    return {
        "cheapest": enrich(cheapest),
        "fastest": enrich(fastest),
        "best_quality": enrich(best_quality),
    }


# ---------------------------------------------------------------------------
# ERP routes
# ---------------------------------------------------------------------------

@router.get("/parts/{part_id}/production-history")
def get_production_history(part_id: str, db: Session = Depends(get_db)):
    _require_part(part_id, db)
    orders = (
        db.query(ProductionOrder)
        .filter(ProductionOrder.part_id == part_id)
        .order_by(ProductionOrder.delivery_date)
        .all()
    )
    return {"part_id": part_id, "orders": [order_to_dict(o) for o in orders]}


@router.get("/parts/{part_id}/cost-summary")
def get_cost_summary(part_id: str, db: Session = Depends(get_db)):
    _require_part(part_id, db)
    orders = db.query(ProductionOrder).filter(ProductionOrder.part_id == part_id).all()
    return {"part_id": part_id, "cost_summary": _cost_summary(orders)}


@router.get("/parts/{part_id}/recommendation")
def get_recommendation(part_id: str, db: Session = Depends(get_db)):
    _require_part(part_id, db)
    orders = db.query(ProductionOrder).filter(ProductionOrder.part_id == part_id).all()
    return {"part_id": part_id, "recommendation": _recommendation(orders, db)}


@router.get("/vendors")
def list_vendors(db: Session = Depends(get_db)):
    vendors = db.query(Vendor).order_by(Vendor.vendor_id).all()
    return {"items": [vendor_to_dict(v) for v in vendors]}


@router.get("/vendors/{vendor_id}")
def get_vendor(vendor_id: str, db: Session = Depends(get_db)):
    vendor = db.get(Vendor, vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail=f"Vendor '{vendor_id}' not found")
    return vendor_to_dict(vendor)


@router.get("/vendors/{vendor_id}/production-history")
def get_vendor_production_history(vendor_id: str, db: Session = Depends(get_db)):
    vendor = db.get(Vendor, vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail=f"Vendor '{vendor_id}' not found")
    orders = (
        db.query(ProductionOrder)
        .filter(ProductionOrder.vendor_id == vendor_id)
        .order_by(ProductionOrder.delivery_date)
        .all()
    )
    return {"vendor_id": vendor_id, "orders": [order_to_dict(o) for o in orders]}


@router.get("/vendors/{vendor_id}/purchase-items")
def get_vendor_purchase_items(vendor_id: str, db: Session = Depends(get_db)):
    vendor = db.get(Vendor, vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail=f"Vendor '{vendor_id}' not found")
    items = (
        db.query(PurchaseItem)
        .filter(PurchaseItem.vendor_id == vendor_id)
        .all()
    )
    return {"vendor_id": vendor_id, "items": [purchase_item_to_dict(i) for i in items]}


# ---------------------------------------------------------------------------
# Bulk query route  (mounted at /query)
# ---------------------------------------------------------------------------

class BulkQueryRequest(BaseModel):
    cad_file_names: list[str]


@query_router.post("/by-cad-files")
def query_by_cad_files(body: BulkQueryRequest, db: Session = Depends(get_db)):
    results = []
    for cad in body.cad_file_names:
        part = db.query(Part).filter(Part.cad_file_name == cad).first()
        if part is None:
            results.append({"cad_file_name": cad, "found": False})
            continue
        orders = (
            db.query(ProductionOrder)
            .filter(ProductionOrder.part_id == part.part_id)
            .order_by(ProductionOrder.delivery_date)
            .all()
        )
        results.append({
            "cad_file_name": cad,
            "found": True,
            "part": part_to_dict(part),
            "production_history": [order_to_dict(o) for o in orders],
            "cost_summary": _cost_summary(orders),
            "recommendation": _recommendation(orders, db),
        })
    return results

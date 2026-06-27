"""
MCP server for PLM/ERP demo.
Run:  uv run mcp_server/server.py
Exposes tools that Claude can call after receiving CAD file names from HOOPS AI MCP.
"""
import sys
from pathlib import Path

# Allow imports from the project root when run directly
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastmcp import FastMCP
from db.database import SessionLocal
from db.models import Part, ProductionOrder, Vendor, Customer

mcp = FastMCP(
    name="PLM ERP Demo",
    instructions=(
        "Use these tools to look up PLM and ERP manufacturing records by CAD file name. "
        "Call query_by_cad_files with the list of CAD file names you received from HOOPS AI "
        "to retrieve part details, production history, cost summaries, and sourcing recommendations."
    ),
)


# ---------------------------------------------------------------------------
# Internal helpers (no DB dependency injection — plain SessionLocal usage)
# ---------------------------------------------------------------------------

def _part_to_dict(p: Part) -> dict:
    return {
        "part_id": p.part_id,
        "part_name": p.part_name,
        "revision": p.revision,
        "material": p.material,
        "weight_kg": p.weight_kg,
        "drawing_number": p.drawing_number,
        "cad_file_name": p.cad_file_name,
        "created_at": str(p.created_at),
        "status": p.status,
    }


def _order_to_dict(o: ProductionOrder) -> dict:
    customer_name = o.customer.company_name if o.customer else None
    return {
        "order_id": o.order_id,
        "production_type": o.production_type,
        "vendor_id": o.vendor_id,
        "customer_id": o.customer_id,
        "customer_name": customer_name,
        "quantity": o.quantity,
        "unit_cost_jpy": o.unit_cost_jpy,
        "lead_time_days": o.lead_time_days,
        "delivery_date": str(o.delivery_date),
        "quality_result": o.quality_result,
        "notes": o.notes,
    }


def _cost_summary(orders: list[ProductionOrder]) -> dict:
    by_type: dict[str, list[float]] = {}
    for o in orders:
        by_type.setdefault(o.production_type, []).append(o.unit_cost_jpy)
    return {
        ptype: {
            "avg_unit_cost_jpy": round(sum(c) / len(c), 2),
            "min_unit_cost_jpy": min(c),
            "max_unit_cost_jpy": max(c),
            "order_count": len(c),
        }
        for ptype, c in by_type.items()
    }


def _recommendation(orders: list[ProductionOrder], db) -> dict:
    if not orders:
        return {}
    buckets: dict[tuple, dict] = {}
    for o in orders:
        key = (o.vendor_id, o.production_type)
        if key not in buckets:
            buckets[key] = {"costs": [], "leads": [], "results": [],
                            "vendor_id": o.vendor_id, "production_type": o.production_type}
        buckets[key]["costs"].append(o.unit_cost_jpy)
        buckets[key]["leads"].append(o.lead_time_days)
        buckets[key]["results"].append(o.quality_result)

    scored = []
    for b in buckets.values():
        pass_rate = b["results"].count("pass") / len(b["results"])
        v = db.get(Vendor, b["vendor_id"]) if b["vendor_id"] else None
        scored.append({
            "vendor_id": b["vendor_id"],
            "vendor_name": v.vendor_name if v else "In-house",
            "production_type": b["production_type"],
            "avg_cost_jpy": round(sum(b["costs"]) / len(b["costs"]), 2),
            "avg_lead_days": round(sum(b["leads"]) / len(b["leads"]), 1),
            "pass_rate": round(pass_rate, 3),
            "sample_count": len(b["costs"]),
        })

    return {
        "cheapest": min(scored, key=lambda x: x["avg_cost_jpy"]),
        "fastest": min(scored, key=lambda x: x["avg_lead_days"]),
        "best_quality": max(scored, key=lambda x: (x["pass_rate"], -x["avg_cost_jpy"])),
    }


# ---------------------------------------------------------------------------
# MCP Tools
# ---------------------------------------------------------------------------

@mcp.tool()
def list_customers() -> list[dict]:
    """Return all customers (取引先/発注元) registered in the system."""
    db = SessionLocal()
    try:
        customers = db.query(Customer).order_by(Customer.customer_id).all()
        return [
            {
                "customer_id": c.customer_id,
                "company_name": c.company_name,
                "contact_name": c.contact_name,
                "address1": c.address1,
                "address2": c.address2,
                "email": c.email,
                "phone": c.phone,
            }
            for c in customers
        ]
    finally:
        db.close()


@mcp.tool()
def get_customer(customer_id: str) -> dict:
    """Return details for a single customer by customer_id."""
    db = SessionLocal()
    try:
        c = db.get(Customer, customer_id)
        if not c:
            return {"found": False, "customer_id": customer_id}
        return {
            "found": True,
            "customer_id": c.customer_id,
            "company_name": c.company_name,
            "contact_name": c.contact_name,
            "address1": c.address1,
            "address2": c.address2,
            "email": c.email,
            "phone": c.phone,
        }
    finally:
        db.close()


@mcp.tool()
def get_part_by_cad_file(cad_file_name: str) -> dict:
    """Look up a part record by its CAD file name (e.g. 'shaft_001.stp')."""
    db = SessionLocal()
    try:
        part = db.query(Part).filter(Part.cad_file_name == cad_file_name).first()
        if not part:
            return {"found": False, "cad_file_name": cad_file_name}
        return {"found": True, "part": _part_to_dict(part)}
    finally:
        db.close()


@mcp.tool()
def get_production_history(part_id: str) -> dict:
    """Return all production orders for a given part_id, sorted by delivery date."""
    db = SessionLocal()
    try:
        orders = (
            db.query(ProductionOrder)
            .filter(ProductionOrder.part_id == part_id)
            .order_by(ProductionOrder.delivery_date)
            .all()
        )
        return {"part_id": part_id, "orders": [_order_to_dict(o) for o in orders]}
    finally:
        db.close()


@mcp.tool()
def get_cost_summary(part_id: str) -> dict:
    """Return average, min, and max unit cost grouped by production_type for a part."""
    db = SessionLocal()
    try:
        orders = db.query(ProductionOrder).filter(ProductionOrder.part_id == part_id).all()
        return {"part_id": part_id, "cost_summary": _cost_summary(orders)}
    finally:
        db.close()


@mcp.tool()
def get_recommendation(part_id: str) -> dict:
    """
    Return cheapest, fastest, and best-quality sourcing options for a part
    based on historical production order data.
    """
    db = SessionLocal()
    try:
        orders = db.query(ProductionOrder).filter(ProductionOrder.part_id == part_id).all()
        return {"part_id": part_id, "recommendation": _recommendation(orders, db)}
    finally:
        db.close()


@mcp.tool()
def query_by_cad_files(cad_file_names: list[str]) -> list[dict]:
    """
    Main tool for Claude's workflow. Given a list of CAD file names from HOOPS AI,
    return part details, full production history, cost summary, and recommendation
    for each file. Files not found in the database are flagged with found=False.
    """
    db = SessionLocal()
    try:
        results = []
        for cad in cad_file_names:
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
                "part": _part_to_dict(part),
                "production_history": [_order_to_dict(o) for o in orders],
                "cost_summary": _cost_summary(orders),
                "recommendation": _recommendation(orders, db),
            })
        return results
    finally:
        db.close()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--http":
        mcp.run(transport="streamable-http", port=8011)
    else:
        mcp.run(transport="stdio")

from typing import Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models import Part, PartStructure

router = APIRouter()


def part_to_dict(p: Part) -> dict[str, Any]:
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


@router.get("/parts")
def list_parts(
    search: Optional[str] = Query(None, description="Search in part_name or drawing_number"),
    status: Optional[str] = Query(None, description="Filter by status: active or obsolete"),
    material: Optional[str] = Query(None, description="Filter by material"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    q = db.query(Part)
    if search:
        like = f"%{search}%"
        q = q.filter(Part.part_name.ilike(like) | Part.drawing_number.ilike(like))
    if status:
        q = q.filter(Part.status == status)
    if material:
        q = q.filter(Part.material == material)
    total = q.count()
    parts = q.order_by(Part.part_id).offset(skip).limit(limit).all()
    return {"total": total, "skip": skip, "limit": limit, "items": [part_to_dict(p) for p in parts]}


@router.get("/parts/{part_id}")
def get_part(part_id: str, db: Session = Depends(get_db)):
    part = db.get(Part, part_id)
    if not part:
        raise HTTPException(status_code=404, detail=f"Part '{part_id}' not found")
    return part_to_dict(part)


@router.get("/parts/by-cad-file/{cad_file_name:path}")
def get_part_by_cad_file(cad_file_name: str, db: Session = Depends(get_db)):
    part = db.query(Part).filter(Part.cad_file_name == cad_file_name).first()
    if not part:
        raise HTTPException(status_code=404, detail=f"No part found for CAD file '{cad_file_name}'")
    return part_to_dict(part)


@router.get("/parts/{part_id}/bom")
def get_bom(part_id: str, db: Session = Depends(get_db)):
    part = db.get(Part, part_id)
    if not part:
        raise HTTPException(status_code=404, detail=f"Part '{part_id}' not found")

    children = (
        db.query(PartStructure)
        .filter(PartStructure.parent_part_id == part_id)
        .all()
    )
    items = []
    for row in children:
        child = db.get(Part, row.child_part_id)
        items.append({
            "child_part_id": row.child_part_id,
            "child_part_name": child.part_name if child else None,
            "child_cad_file_name": child.cad_file_name if child else None,
            "quantity": row.quantity,
        })
    return {"part_id": part_id, "bom": items}


@router.get("/parts/{part_id}/where-used")
def get_where_used(part_id: str, db: Session = Depends(get_db)):
    part = db.get(Part, part_id)
    if not part:
        raise HTTPException(status_code=404, detail=f"Part '{part_id}' not found")

    parents = (
        db.query(PartStructure)
        .filter(PartStructure.child_part_id == part_id)
        .all()
    )
    items = []
    for row in parents:
        parent = db.get(Part, row.parent_part_id)
        items.append({
            "parent_part_id": row.parent_part_id,
            "parent_part_name": parent.part_name if parent else None,
            "parent_cad_file_name": parent.cad_file_name if parent else None,
            "quantity": row.quantity,
        })
    return {"part_id": part_id, "where_used": items}

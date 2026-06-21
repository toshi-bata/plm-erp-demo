from typing import Any
from fastapi import APIRouter, Depends, HTTPException
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

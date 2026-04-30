from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.auth import get_current_admin
from backend.database import get_db
from backend.models import AdminUser, Certification
from backend.schemas import CertificationCreate, CertificationResponse, CertificationUpdate

router = APIRouter(prefix="/certifications", tags=["certifications"])


@router.get("/", response_model=List[CertificationResponse])
def list_certifications(db: Session = Depends(get_db)):
    return db.query(Certification).order_by(Certification.order).all()


@router.post("/", response_model=CertificationResponse)
def create_certification(
    payload: CertificationCreate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    item = Certification(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{item_id}", response_model=CertificationResponse)
def update_certification(
    item_id: int,
    payload: CertificationUpdate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    item = db.query(Certification).filter(Certification.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}")
def delete_certification(
    item_id: int,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    item = db.query(Certification).filter(Certification.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(item)
    db.commit()
    return {"ok": True}

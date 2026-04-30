from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.auth import get_current_admin
from backend.database import get_db
from backend.models import AdminUser, ImpactMetric
from backend.schemas import ImpactMetricCreate, ImpactMetricResponse, ImpactMetricUpdate

router = APIRouter(prefix="/impact", tags=["impact"])


@router.get("/", response_model=List[ImpactMetricResponse])
def list_impact(db: Session = Depends(get_db)):
    return db.query(ImpactMetric).order_by(ImpactMetric.order).all()


@router.post("/", response_model=ImpactMetricResponse)
def create_impact(
    payload: ImpactMetricCreate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    item = ImpactMetric(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{item_id}", response_model=ImpactMetricResponse)
def update_impact(
    item_id: int,
    payload: ImpactMetricUpdate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    item = db.query(ImpactMetric).filter(ImpactMetric.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}")
def delete_impact(
    item_id: int,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    item = db.query(ImpactMetric).filter(ImpactMetric.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(item)
    db.commit()
    return {"ok": True}

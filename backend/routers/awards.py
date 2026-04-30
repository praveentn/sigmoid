from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.auth import get_current_admin
from backend.database import get_db
from backend.models import AdminUser, Award
from backend.schemas import AwardCreate, AwardResponse, AwardUpdate

router = APIRouter(prefix="/awards", tags=["awards"])


@router.get("/", response_model=List[AwardResponse])
def list_awards(db: Session = Depends(get_db)):
    return db.query(Award).order_by(Award.order).all()


@router.post("/", response_model=AwardResponse)
def create_award(
    payload: AwardCreate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    item = Award(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{item_id}", response_model=AwardResponse)
def update_award(
    item_id: int,
    payload: AwardUpdate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    item = db.query(Award).filter(Award.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}")
def delete_award(
    item_id: int,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    item = db.query(Award).filter(Award.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(item)
    db.commit()
    return {"ok": True}

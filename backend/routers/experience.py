from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.auth import get_current_admin
from backend.database import get_db
from backend.models import AdminUser, Experience
from backend.schemas import ExperienceCreate, ExperienceResponse, ExperienceUpdate

router = APIRouter(prefix="/experience", tags=["experience"])


@router.get("/", response_model=List[ExperienceResponse])
def list_experience(db: Session = Depends(get_db)):
    return db.query(Experience).order_by(Experience.order).all()


@router.post("/", response_model=ExperienceResponse)
def create_experience(
    payload: ExperienceCreate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    item = Experience(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{item_id}", response_model=ExperienceResponse)
def update_experience(
    item_id: int,
    payload: ExperienceUpdate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    item = db.query(Experience).filter(Experience.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}")
def delete_experience(
    item_id: int,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    item = db.query(Experience).filter(Experience.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(item)
    db.commit()
    return {"ok": True}

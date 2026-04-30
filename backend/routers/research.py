from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.auth import get_current_admin
from backend.database import get_db
from backend.models import AdminUser, Research
from backend.schemas import ResearchCreate, ResearchResponse, ResearchUpdate

router = APIRouter(prefix="/research", tags=["research"])


@router.get("/", response_model=List[ResearchResponse])
def list_research(db: Session = Depends(get_db)):
    return db.query(Research).order_by(Research.order).all()


@router.post("/", response_model=ResearchResponse)
def create_research(
    payload: ResearchCreate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    item = Research(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{item_id}", response_model=ResearchResponse)
def update_research(
    item_id: int,
    payload: ResearchUpdate,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    item = db.query(Research).filter(Research.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}")
def delete_research(
    item_id: int,
    db: Session = Depends(get_db),
    _: AdminUser = Depends(get_current_admin),
):
    item = db.query(Research).filter(Research.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(item)
    db.commit()
    return {"ok": True}

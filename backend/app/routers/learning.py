from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.learning_progress import LearningProgress
from app.models.user import User
from app.schemas.learning import (
    LearningProgressCreate,
    LearningProgressResponse,
    LearningProgressUpdate,
)

router = APIRouter(prefix="/learning", tags=["Learning Tracker"])


@router.get("", response_model=list[LearningProgressResponse])
def list_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(LearningProgress)
        .filter(LearningProgress.user_id == current_user.id)
        .order_by(LearningProgress.created_at.desc())
        .all()
    )


@router.post("", response_model=LearningProgressResponse)
def create_progress(
    data: LearningProgressCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    item = LearningProgress(user_id=current_user.id, **data.model_dump())
    if data.status == "completed":
        item.completed_at = datetime.utcnow()
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{item_id}", response_model=LearningProgressResponse)
def update_progress(
    item_id: int,
    data: LearningProgressUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    item = (
        db.query(LearningProgress)
        .filter(LearningProgress.id == item_id, LearningProgress.user_id == current_user.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    if data.status == "completed" and not item.completed_at:
        item.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}")
def delete_progress(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    item = (
        db.query(LearningProgress)
        .filter(LearningProgress.id == item_id, LearningProgress.user_id == current_user.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Item deleted"}

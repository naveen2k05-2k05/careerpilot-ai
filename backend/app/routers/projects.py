from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.project import Project, UserProject
from app.models.user import User
from app.services.gemini import recommend_projects

router = APIRouter(prefix="/projects", tags=["Projects"])


class SaveProjectRequest(BaseModel):
    title: str
    project_id: int | None = None
    status: str = "recommended"


class UpdateUserProjectRequest(BaseModel):
    status: str


@router.get("/recommendations")
def get_recommendations(
    target_role: str = Query(...),
    current_user: User = Depends(get_current_user),
):
    return recommend_projects(target_role)


@router.get("/catalog")
def get_catalog(
    target_role: str | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Project)
    if target_role:
        query = query.filter(Project.target_role == target_role)
    return query.all()


@router.get("/my")
def get_my_projects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(UserProject)
        .filter(UserProject.user_id == current_user.id)
        .order_by(UserProject.created_at.desc())
        .all()
    )


@router.post("/my")
def save_project(
    data: SaveProjectRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    item = UserProject(
        user_id=current_user.id,
        project_id=data.project_id,
        title=data.title,
        status=data.status,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/my/{item_id}")
def update_my_project(
    item_id: int,
    data: UpdateUserProjectRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    item = (
        db.query(UserProject)
        .filter(UserProject.id == item_id, UserProject.user_id == current_user.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Project not found")
    item.status = data.status
    if data.status == "completed":
        item.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(item)
    return item


@router.delete("/my/{item_id}")
def delete_my_project(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    item = (
        db.query(UserProject)
        .filter(UserProject.id == item_id, UserProject.user_id == current_user.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(item)
    db.commit()
    return {"message": "Project removed"}

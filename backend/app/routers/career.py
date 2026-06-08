from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.career_roadmap import CareerRoadmap
from app.models.user import User
from app.schemas.career import CareerRoadmapRequest, CareerRoadmapResponse
from app.services.gemini import ROLES, generate_career_roadmap

router = APIRouter(prefix="/career", tags=["Career Coach"])


@router.get("/roles")
def get_roles():
    return {"roles": ROLES}


@router.get("/roadmaps", response_model=list[CareerRoadmapResponse])
def list_roadmaps(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(CareerRoadmap)
        .filter(CareerRoadmap.user_id == current_user.id)
        .order_by(CareerRoadmap.created_at.desc())
        .all()
    )


@router.post("/roadmap", response_model=CareerRoadmapResponse)
def create_roadmap(
    data: CareerRoadmapRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = generate_career_roadmap(data.target_role)
    roadmap = CareerRoadmap(
        user_id=current_user.id,
        target_role=data.target_role,
        required_skills=result.get("required_skills"),
        learning_roadmap=result.get("learning_roadmap"),
        recommended_courses=result.get("recommended_courses"),
        recommended_projects=result.get("recommended_projects"),
        estimated_timeline=result.get("estimated_timeline"),
    )
    db.add(roadmap)
    current_user.target_role = data.target_role
    db.commit()
    db.refresh(roadmap)
    return roadmap

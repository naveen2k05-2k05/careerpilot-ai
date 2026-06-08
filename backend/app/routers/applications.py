from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.job_application import JobApplication
from app.models.user import User
from app.schemas.job import JobApplicationCreate, JobApplicationResponse, JobApplicationUpdate

router = APIRouter(prefix="/applications", tags=["Job Applications"])

VALID_STATUSES = ["applied", "under_review", "interview_scheduled", "rejected", "offer_received"]


@router.get("", response_model=list[JobApplicationResponse])
def list_applications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(JobApplication)
        .filter(JobApplication.user_id == current_user.id)
        .order_by(JobApplication.application_date.desc())
        .all()
    )


@router.post("", response_model=JobApplicationResponse)
def create_application(
    data: JobApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if data.status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail=f"Invalid status. Use: {VALID_STATUSES}")

    app_data = data.model_dump()
    application = JobApplication(user_id=current_user.id, **app_data)
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


@router.put("/{app_id}", response_model=JobApplicationResponse)
def update_application(
    app_id: int,
    data: JobApplicationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    application = (
        db.query(JobApplication)
        .filter(JobApplication.id == app_id, JobApplication.user_id == current_user.id)
        .first()
    )
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        if field == "status" and value not in VALID_STATUSES:
            raise HTTPException(status_code=400, detail=f"Invalid status. Use: {VALID_STATUSES}")
        setattr(application, field, value)

    db.commit()
    db.refresh(application)
    return application


@router.delete("/{app_id}")
def delete_application(
    app_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    application = (
        db.query(JobApplication)
        .filter(JobApplication.id == app_id, JobApplication.user_id == current_user.id)
        .first()
    )
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    db.delete(application)
    db.commit()
    return {"message": "Application deleted"}

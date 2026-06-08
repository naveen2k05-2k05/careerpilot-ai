from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.interview import Interview
from app.models.interview_feedback import InterviewFeedback
from app.models.job_application import JobApplication
from app.models.learning_progress import LearningProgress
from app.models.resume import Resume
from app.models.user import User
from app.models.skill import UserSkill
from app.schemas.analytics import DashboardResponse
from app.services.gemini import get_dashboard_recommendations

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("", response_model=DashboardResponse)
def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    latest_resume = (
        db.query(Resume)
        .filter(Resume.user_id == current_user.id)
        .order_by(Resume.created_at.desc())
        .first()
    )
    resume_score = latest_resume.ats_score if latest_resume and latest_resume.ats_score else 0.0

    feedbacks = (
        db.query(InterviewFeedback)
        .join(Interview)
        .filter(Interview.user_id == current_user.id)
        .all()
    )
    if feedbacks:
        interview_readiness = sum(f.overall_rating for f in feedbacks) / len(feedbacks)
    else:
        interview_readiness = 0.0

    skills = db.query(UserSkill).filter(UserSkill.user_id == current_user.id).all()
    if skills:
        skills_progress = sum(s.proficiency / max(s.target_proficiency, 1) * 100 for s in skills) / len(skills)
    else:
        completed_learning = (
            db.query(LearningProgress)
            .filter(LearningProgress.user_id == current_user.id, LearningProgress.status == "completed")
            .count()
        )
        skills_progress = min(completed_learning * 10, 100)

    applications_count = (
        db.query(JobApplication).filter(JobApplication.user_id == current_user.id).count()
    )

    upcoming = (
        db.query(Interview)
        .filter(
            Interview.user_id == current_user.id,
            Interview.scheduled_at.isnot(None),
            Interview.scheduled_at >= datetime.utcnow(),
        )
        .order_by(Interview.scheduled_at)
        .limit(5)
        .all()
    )
    upcoming_interviews = [
        {
            "id": i.id,
            "title": i.title,
            "scheduled_at": i.scheduled_at.isoformat() if i.scheduled_at else None,
            "target_role": i.target_role,
        }
        for i in upcoming
    ]

    if not upcoming_interviews:
        recent_apps = (
            db.query(JobApplication)
            .filter(
                JobApplication.user_id == current_user.id,
                JobApplication.status == "interview_scheduled",
            )
            .limit(3)
            .all()
        )
        upcoming_interviews = [
            {
                "id": a.id,
                "title": f"Interview at {a.company_name}",
                "scheduled_at": (a.application_date + timedelta(days=7)).isoformat(),
                "target_role": a.role,
            }
            for a in recent_apps
        ]

    recommendations = get_dashboard_recommendations(
        {
            "resume_score": resume_score,
            "interview_readiness": interview_readiness,
            "applications_count": applications_count,
            "target_role": current_user.target_role,
        }
    )

    return DashboardResponse(
        resume_score=resume_score,
        interview_readiness=interview_readiness,
        skills_progress=skills_progress,
        applications_count=applications_count,
        upcoming_interviews=upcoming_interviews,
        recommendations=recommendations,
    )

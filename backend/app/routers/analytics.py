from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.interview import Interview
from app.models.interview_feedback import InterviewFeedback
from app.models.job_application import JobApplication
from app.models.learning_progress import LearningProgress
from app.models.resume import Resume
from app.models.skill import UserSkill
from app.models.user import User
from app.schemas.analytics import AnalyticsResponse

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("", response_model=AnalyticsResponse)
def get_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    skills = db.query(UserSkill).filter(UserSkill.user_id == current_user.id).all()
    skill_progress = [
        {"skill": s.skill_name, "proficiency": s.proficiency, "target": s.target_proficiency}
        for s in skills
    ]
    if not skill_progress:
        learning = db.query(LearningProgress).filter(
            LearningProgress.user_id == current_user.id, LearningProgress.item_type == "skill"
        ).all()
        skill_progress = [{"skill": l.title, "proficiency": 50 if l.status == "completed" else 25, "target": 100} for l in learning]

    resumes = (
        db.query(Resume)
        .filter(Resume.user_id == current_user.id, Resume.ats_score.isnot(None))
        .order_by(Resume.created_at)
        .all()
    )
    ats_improvement = [
        {"date": r.created_at.strftime("%Y-%m-%d"), "score": r.ats_score}
        for r in resumes
    ]

    feedbacks = (
        db.query(InterviewFeedback)
        .join(Interview)
        .filter(Interview.user_id == current_user.id)
        .order_by(InterviewFeedback.created_at)
        .all()
    )
    interview_scores = [
        {
            "date": f.created_at.strftime("%Y-%m-%d"),
            "technical": f.technical_score,
            "communication": f.communication_score,
            "confidence": f.confidence_score,
            "overall": f.overall_rating,
        }
        for f in feedbacks
    ]

    applications = db.query(JobApplication).filter(JobApplication.user_id == current_user.id).all()
    total = len(applications)
    offers = sum(1 for a in applications if a.status == "offer_received")
    interviews = sum(1 for a in applications if a.status == "interview_scheduled")
    rejected = sum(1 for a in applications if a.status == "rejected")

    application_success_rate = {
        "total": total,
        "offers": offers,
        "interviews": interviews,
        "rejected": rejected,
        "success_rate": round((offers / total * 100) if total else 0, 1),
        "interview_rate": round((interviews / total * 100) if total else 0, 1),
    }

    return AnalyticsResponse(
        skill_progress=skill_progress,
        ats_improvement=ats_improvement,
        interview_scores=interview_scores,
        application_success_rate=application_success_rate,
    )

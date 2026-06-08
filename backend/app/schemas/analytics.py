from pydantic import BaseModel


class DashboardResponse(BaseModel):
    resume_score: float
    interview_readiness: float
    skills_progress: float
    applications_count: int
    upcoming_interviews: list
    recommendations: list[str]


class AnalyticsResponse(BaseModel):
    skill_progress: list[dict]
    ats_improvement: list[dict]
    interview_scores: list[dict]
    application_success_rate: dict

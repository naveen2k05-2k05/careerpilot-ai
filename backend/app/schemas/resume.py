from datetime import datetime
from pydantic import BaseModel


class ResumeResponse(BaseModel):
    id: int
    filename: str
    ats_score: float | None
    strengths: list | None
    weaknesses: list | None
    improvements: list | None
    extracted_skills: list | None
    missing_skills: list | None
    created_at: datetime

    class Config:
        from_attributes = True


class ResumeAnalysisResponse(BaseModel):
    resume: ResumeResponse
    message: str = "Resume analyzed successfully"

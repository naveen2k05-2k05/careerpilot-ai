from datetime import datetime
from pydantic import BaseModel


class CareerRoadmapRequest(BaseModel):
    target_role: str


class CareerRoadmapResponse(BaseModel):
    id: int
    target_role: str
    required_skills: list | None
    learning_roadmap: list | None
    recommended_courses: list | None
    recommended_projects: list | None
    estimated_timeline: str | None
    created_at: datetime

    class Config:
        from_attributes = True

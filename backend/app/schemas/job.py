from datetime import datetime
from pydantic import BaseModel


class JobApplicationCreate(BaseModel):
    company_name: str
    role: str
    status: str = "applied"
    notes: str | None = None
    application_date: datetime | None = None


class JobApplicationUpdate(BaseModel):
    company_name: str | None = None
    role: str | None = None
    status: str | None = None
    notes: str | None = None


class JobApplicationResponse(BaseModel):
    id: int
    company_name: str
    role: str
    status: str
    application_date: datetime
    notes: str | None
    match_percentage: float | None
    created_at: datetime

    class Config:
        from_attributes = True


class JobMatchRequest(BaseModel):
    job_description: str
    resume_id: int | None = None
    company_name: str | None = None
    role: str | None = None
    save_application: bool = False

from datetime import datetime
from pydantic import BaseModel


class LearningProgressCreate(BaseModel):
    item_type: str
    title: str
    description: str | None = None
    status: str = "in_progress"


class LearningProgressUpdate(BaseModel):
    status: str | None = None
    title: str | None = None


class LearningProgressResponse(BaseModel):
    id: int
    item_type: str
    title: str
    description: str | None
    status: str
    completed_at: datetime | None
    created_at: datetime

    class Config:
        from_attributes = True

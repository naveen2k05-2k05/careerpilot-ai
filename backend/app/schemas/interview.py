from datetime import datetime
from pydantic import BaseModel


class InterviewCreate(BaseModel):
    title: str = "Mock Interview"
    difficulty: str = "intermediate"
    target_role: str | None = None


class InterviewQuestionRequest(BaseModel):
    target_role: str
    difficulty: str = "intermediate"
    question_types: list[str] | None = None


class MockInterviewMessage(BaseModel):
    content: str


class InterviewMessageResponse(BaseModel):
    id: int
    role: str
    content: str
    evaluation: dict | None
    is_follow_up: bool
    created_at: datetime

    class Config:
        from_attributes = True


class InterviewResponse(BaseModel):
    id: int
    title: str
    interview_type: str
    difficulty: str
    target_role: str | None
    status: str
    questions: list | None
    scheduled_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
    messages: list[InterviewMessageResponse] = []

    class Config:
        from_attributes = True


class InterviewFeedbackResponse(BaseModel):
    id: int
    technical_score: float
    communication_score: float
    confidence_score: float
    overall_rating: float
    improvement_suggestions: list | None
    detailed_feedback: str | None
    created_at: datetime

    class Config:
        from_attributes = True

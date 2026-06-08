from datetime import datetime
from sqlalchemy import DateTime, Integer, ForeignKey, Float, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class InterviewFeedback(Base):
    __tablename__ = "interview_feedback"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    interview_id: Mapped[int] = mapped_column(
        ForeignKey("interviews.id", ondelete="CASCADE"), unique=True
    )
    technical_score: Mapped[float] = mapped_column(Float, default=0.0)
    communication_score: Mapped[float] = mapped_column(Float, default=0.0)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0)
    overall_rating: Mapped[float] = mapped_column(Float, default=0.0)
    improvement_suggestions: Mapped[list | None] = mapped_column(JSON, nullable=True)
    detailed_feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    interview = relationship("Interview", back_populates="feedback")

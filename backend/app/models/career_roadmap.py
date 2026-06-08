from datetime import datetime
from sqlalchemy import String, DateTime, Integer, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class CareerRoadmap(Base):
    __tablename__ = "career_roadmaps"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    target_role: Mapped[str] = mapped_column(String(100))
    required_skills: Mapped[list | None] = mapped_column(JSON, nullable=True)
    learning_roadmap: Mapped[list | None] = mapped_column(JSON, nullable=True)
    recommended_courses: Mapped[list | None] = mapped_column(JSON, nullable=True)
    recommended_projects: Mapped[list | None] = mapped_column(JSON, nullable=True)
    estimated_timeline: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="roadmaps")

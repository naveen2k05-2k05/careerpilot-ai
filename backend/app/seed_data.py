from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.career_roadmap import CareerRoadmap
from app.models.interview import Interview, InterviewMessage
from app.models.interview_feedback import InterviewFeedback
from app.models.job_application import JobApplication
from app.models.learning_progress import LearningProgress
from app.models.project import Project
from app.models.resume import Resume
from app.models.skill import UserSkill

SAMPLE_PROJECTS = [
    {
        "title": "Personal Portfolio Website",
        "description": "Build a responsive portfolio with React and deploy to Netlify.",
        "technologies": ["React", "Tailwind CSS", "Netlify"],
        "difficulty": "beginner",
        "target_role": "Full Stack Developer",
        "resume_impact": "Demonstrates frontend skills and deployment experience.",
    },
    {
        "title": "REST API with Authentication",
        "description": "Create a FastAPI backend with JWT auth and PostgreSQL.",
        "technologies": ["Python", "FastAPI", "PostgreSQL"],
        "difficulty": "intermediate",
        "target_role": "Software Engineer",
        "resume_impact": "Shows backend architecture and security knowledge.",
    },
    {
        "title": "ML Prediction Pipeline",
        "description": "End-to-end machine learning pipeline with model serving.",
        "technologies": ["Python", "scikit-learn", "Docker"],
        "difficulty": "advanced",
        "target_role": "Data Scientist",
        "resume_impact": "Highlights ML engineering and MLOps capabilities.",
    },
    {
        "title": "Data Dashboard",
        "description": "Interactive analytics dashboard with Chart.js and SQL queries.",
        "technologies": ["JavaScript", "Chart.js", "SQL"],
        "difficulty": "beginner",
        "target_role": "Data Analyst",
        "resume_impact": "Proves data visualization and SQL proficiency.",
    },
    {
        "title": "RAG Chatbot",
        "description": "Retrieval-augmented generation chatbot using Gemini API.",
        "technologies": ["Python", "Gemini API", "Vector DB"],
        "difficulty": "advanced",
        "target_role": "AI Engineer",
        "resume_impact": "Demonstrates cutting-edge AI integration skills.",
    },
]


def seed_catalog_projects(db: Session):
    if db.query(Project).count() == 0:
        for p in SAMPLE_PROJECTS:
            db.add(Project(**p))
        db.commit()


def seed_demo_user_data(db: Session, user_id: int):
    if db.query(Resume).filter(Resume.user_id == user_id).first():
        return

    db.add(Resume(
        user_id=user_id,
        filename="demo_resume.pdf",
        extracted_text="Demo resume for CareerPilot AI",
        ats_score=78.0,
        strengths=["Clear structure", "Relevant technical skills", "Project experience"],
        weaknesses=["Missing quantified achievements", "Limited ATS keywords"],
        improvements=["Add metrics to projects", "Include role-specific keywords"],
        extracted_skills=["Python", "JavaScript", "React", "SQL", "Git"],
        missing_skills=["Docker", "AWS", "System Design"],
    ))

    for skill, prof in [("Python", 85), ("JavaScript", 75), ("React", 70), ("SQL", 80), ("Git", 90)]:
        db.add(UserSkill(user_id=user_id, skill_name=skill, proficiency=prof, target_proficiency=100))

    db.add(CareerRoadmap(
        user_id=user_id,
        target_role="Software Engineer",
        required_skills=["Python", "SQL", "Git", "Data Structures", "APIs"],
        learning_roadmap=[
            {"phase": "Foundation", "duration": "4-6 weeks", "topics": ["Programming", "Git", "SQL"]},
            {"phase": "Core Skills", "duration": "8-10 weeks", "topics": ["Frameworks", "Testing"]},
        ],
        recommended_courses=[
            {"name": "Software Engineering Fundamentals", "platform": "Coursera", "url": "https://coursera.org"},
        ],
        recommended_projects=[{"title": "Portfolio API", "description": "REST API with auth"}],
        estimated_timeline="6-9 months",
    ))

    applications = [
        ("Google", "Software Engineer", "interview_scheduled"),
        ("Microsoft", "Full Stack Developer", "under_review"),
        ("Startup Inc", "Backend Engineer", "applied"),
        ("Meta", "SWE Intern", "rejected"),
        ("Amazon", "SDE I", "offer_received"),
    ]
    for i, (company, role, status) in enumerate(applications):
        db.add(JobApplication(
            user_id=user_id,
            company_name=company,
            role=role,
            status=status,
            application_date=datetime.utcnow() - timedelta(days=14 - i * 3),
            notes=f"Applied via careers portal",
        ))

    learning_items = [
        ("skill", "Docker", "completed"),
        ("course", "System Design Basics", "completed"),
        ("project", "Portfolio API", "in_progress"),
        ("skill", "AWS", "in_progress"),
        ("interview", "Mock Interview Practice", "completed"),
    ]
    for item_type, title, status in learning_items:
        item = LearningProgress(user_id=user_id, item_type=item_type, title=title, status=status)
        if status == "completed":
            item.completed_at = datetime.utcnow() - timedelta(days=5)
        db.add(item)

    interview = Interview(
        user_id=user_id,
        title="Software Engineer Mock Interview",
        interview_type="mock",
        difficulty="intermediate",
        target_role="Software Engineer",
        status="completed",
        completed_at=datetime.utcnow() - timedelta(days=3),
    )
    db.add(interview)
    db.flush()

    db.add(InterviewMessage(interview_id=interview.id, role="interviewer", content="Tell me about yourself."))
    db.add(InterviewMessage(
        interview_id=interview.id,
        role="candidate",
        content="I am a software engineer with experience in Python and React...",
    ))
    db.add(InterviewFeedback(
        interview_id=interview.id,
        technical_score=78.0,
        communication_score=82.0,
        confidence_score=74.0,
        overall_rating=78.0,
        improvement_suggestions=[
            "Use the STAR method for behavioral questions",
            "Add more technical depth in answers",
        ],
        detailed_feedback="Solid performance with room to improve specificity.",
    ))

    db.add(Resume(
        user_id=user_id,
        filename="resume_v1.pdf",
        ats_score=65.0,
        extracted_skills=["Python", "Java"],
        created_at=datetime.utcnow() - timedelta(days=30),
    ))

    db.commit()


def seed_sample_data():
    db: Session = SessionLocal()
    try:
        seed_catalog_projects(db)
    except Exception:
        db.rollback()
    finally:
        db.close()

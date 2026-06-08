from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.firebase import init_firebase
from app.config import get_settings
from app.database import Base, engine
from app.routers import (
    analytics,
    applications,
    auth,
    career,
    dashboard,
    interview,
    job_match,
    learning,
    projects,
    resume,
)
from app.seed_data import seed_sample_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    init_firebase()
    seed_sample_data()
    yield


settings = get_settings()

app = FastAPI(
    title="CareerPilot AI API",
    description="AI-powered Career Coach and Interview Preparation Platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(resume.router, prefix="/api")
app.include_router(career.router, prefix="/api")
app.include_router(interview.router, prefix="/api")
app.include_router(job_match.router, prefix="/api")
app.include_router(projects.router, prefix="/api")
app.include_router(applications.router, prefix="/api")
app.include_router(learning.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "CareerPilot AI API", "docs": "/docs", "health": "/health"}


@app.get("/health")
def health():
    return {"status": "healthy"}

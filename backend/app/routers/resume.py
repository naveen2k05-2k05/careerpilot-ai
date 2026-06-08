from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.resume import Resume
from app.models.skill import UserSkill
from app.models.user import User
from app.schemas.resume import ResumeAnalysisResponse, ResumeResponse
from app.services.gemini import analyze_resume
from app.services.resume_parser import extract_resume_text

router = APIRouter(prefix="/resumes", tags=["Resume"])


@router.get("", response_model=list[ResumeResponse])
def list_resumes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(Resume).filter(Resume.user_id == current_user.id).order_by(Resume.created_at.desc()).all()


@router.get("/{resume_id}", response_model=ResumeResponse)
def get_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume


@router.post("/upload", response_model=ResumeAnalysisResponse)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    content = await file.read()
    try:
        text = extract_resume_text(file.filename, content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    analysis = analyze_resume(text, current_user.target_role)

    resume = Resume(
        user_id=current_user.id,
        filename=file.filename,
        extracted_text=text,
        ats_score=analysis.get("ats_score"),
        strengths=analysis.get("strengths"),
        weaknesses=analysis.get("weaknesses"),
        improvements=analysis.get("improvements"),
        extracted_skills=analysis.get("extracted_skills"),
        missing_skills=analysis.get("missing_skills"),
    )
    db.add(resume)
    db.flush()

    for skill_name in analysis.get("extracted_skills") or []:
        existing = (
            db.query(UserSkill)
            .filter(UserSkill.user_id == current_user.id, UserSkill.skill_name == skill_name)
            .first()
        )
        if existing:
            existing.proficiency = min(existing.proficiency + 5, 100)
        else:
            db.add(UserSkill(user_id=current_user.id, skill_name=skill_name, proficiency=60.0))

    db.commit()
    db.refresh(resume)
    return ResumeAnalysisResponse(resume=resume)

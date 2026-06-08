from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.job_application import JobApplication
from app.models.resume import Resume
from app.models.user import User
from app.schemas.job import JobMatchRequest
from app.services.gemini import analyze_job_match
from app.services.resume_parser import extract_resume_text

router = APIRouter(prefix="/job-match", tags=["Job Match"])


@router.post("/analyze")
async def analyze_match(
    data: JobMatchRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    resume_text = ""
    if data.resume_id:
        resume = (
            db.query(Resume)
            .filter(Resume.id == data.resume_id, Resume.user_id == current_user.id)
            .first()
        )
        if not resume or not resume.extracted_text:
            raise HTTPException(status_code=404, detail="Resume not found")
        resume_text = resume.extracted_text
    else:
        latest = (
            db.query(Resume)
            .filter(Resume.user_id == current_user.id)
            .order_by(Resume.created_at.desc())
            .first()
        )
        if latest and latest.extracted_text:
            resume_text = latest.extracted_text
        else:
            raise HTTPException(status_code=400, detail="Please upload a resume first")

    result = analyze_job_match(resume_text, data.job_description)

    if data.save_application and data.company_name and data.role:
        application = JobApplication(
            user_id=current_user.id,
            company_name=data.company_name,
            role=data.role,
            status="applied",
            job_description=data.job_description,
            match_percentage=result.get("match_percentage"),
            gap_analysis=result,
            notes="Created from job match analysis",
        )
        db.add(application)
        db.commit()

    return result


@router.post("/analyze-upload")
async def analyze_match_upload(
    job_description: str = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    content = await file.read()
    try:
        resume_text = extract_resume_text(file.filename, content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    result = analyze_job_match(resume_text, job_description)
    return result

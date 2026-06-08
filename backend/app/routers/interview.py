from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.interview import Interview, InterviewMessage
from app.models.interview_feedback import InterviewFeedback
from app.models.learning_progress import LearningProgress
from app.models.user import User
from app.schemas.interview import (
    InterviewCreate,
    InterviewFeedbackResponse,
    InterviewQuestionRequest,
    InterviewResponse,
    MockInterviewMessage,
)
from app.services.gemini import (
    evaluate_interview_answer,
    generate_interview_feedback,
    generate_interview_questions,
    get_mock_interview_question,
)

router = APIRouter(prefix="/interviews", tags=["Interview"])


@router.get("", response_model=list[InterviewResponse])
def list_interviews(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(Interview)
        .filter(Interview.user_id == current_user.id)
        .order_by(Interview.created_at.desc())
        .all()
    )


@router.post("/questions")
def create_questions(
    data: InterviewQuestionRequest,
    current_user: User = Depends(get_current_user),
):
    questions = generate_interview_questions(
        data.target_role, data.difficulty, data.question_types
    )
    return {"questions": questions}


@router.post("", response_model=InterviewResponse)
def start_mock_interview(
    data: InterviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    role = data.target_role or current_user.target_role or "Software Engineer"
    first_question = get_mock_interview_question(role, data.difficulty, [], 0)

    interview = Interview(
        user_id=current_user.id,
        title=data.title,
        interview_type="mock",
        difficulty=data.difficulty,
        target_role=role,
        status="in_progress",
    )
    db.add(interview)
    db.flush()

    msg = InterviewMessage(interview_id=interview.id, role="interviewer", content=first_question)
    db.add(msg)
    db.commit()
    interview = (
        db.query(Interview)
        .options(joinedload(Interview.messages))
        .filter(Interview.id == interview.id)
        .first()
    )
    return interview


@router.get("/{interview_id}", response_model=InterviewResponse)
def get_interview(
    interview_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    interview = (
        db.query(Interview)
        .filter(Interview.id == interview_id, Interview.user_id == current_user.id)
        .first()
    )
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    return interview


@router.post("/{interview_id}/message")
def send_message(
    interview_id: int,
    data: MockInterviewMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    interview = (
        db.query(Interview)
        .filter(Interview.id == interview_id, Interview.user_id == current_user.id)
        .first()
    )
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    if interview.status != "in_progress":
        raise HTTPException(status_code=400, detail="Interview is not in progress")

    messages = (
        db.query(InterviewMessage)
        .filter(InterviewMessage.interview_id == interview_id)
        .order_by(InterviewMessage.created_at)
        .all()
    )

    last_interviewer = next((m for m in reversed(messages) if m.role == "interviewer"), None)
    question = last_interviewer.content if last_interviewer else ""

    evaluation = evaluate_interview_answer(
        question, data.content, interview.target_role or "Software Engineer", interview.difficulty
    )

    user_msg = InterviewMessage(
        interview_id=interview_id,
        role="candidate",
        content=data.content,
        evaluation=evaluation,
    )
    db.add(user_msg)
    db.flush()

    conversation = [{"role": m.role, "content": m.content} for m in messages]
    conversation.append({"role": "candidate", "content": data.content})

    interviewer_count = sum(1 for m in messages if m.role == "interviewer")
    # Check if needs clarification (user gave unclear answer)
    needs_clarification = evaluation.get("needs_clarification", False)
    
    if needs_clarification:
        # Don't increment question count, ask for clarification
        next_content = None
        is_follow_up = False
    elif interviewer_count >= 10:
        # Stop after 10 questions
        next_content = None
        is_follow_up = False
    else:
        next_content = get_mock_interview_question(
            interview.target_role or "Software Engineer",
            interview.difficulty,
            conversation,
            interviewer_count,
        )
        is_follow_up = False

    # Only mark as complete if we've reached 10 questions, not for clarification
    is_complete = interviewer_count >= 10 and not needs_clarification
    response = {"evaluation": evaluation, "interview_complete": is_complete}

    if next_content:
        interviewer_msg = InterviewMessage(
            interview_id=interview_id,
            role="interviewer",
            content=next_content,
            is_follow_up=is_follow_up,
        )
        db.add(interviewer_msg)
        response["next_question"] = next_content
    elif is_complete:
        interview.status = "completed"
        interview.completed_at = datetime.utcnow()

    db.commit()
    return response


@router.post("/{interview_id}/complete", response_model=InterviewFeedbackResponse)
def complete_interview(
    interview_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    interview = (
        db.query(Interview)
        .filter(Interview.id == interview_id, Interview.user_id == current_user.id)
        .first()
    )
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    existing = db.query(InterviewFeedback).filter(InterviewFeedback.interview_id == interview_id).first()
    if existing:
        return existing

    messages = (
        db.query(InterviewMessage)
        .filter(InterviewMessage.interview_id == interview_id)
        .order_by(InterviewMessage.created_at)
        .all()
    )
    conversation = [{"role": m.role, "content": m.content} for m in messages]
    feedback_data = generate_interview_feedback(
        conversation, interview.target_role or "Software Engineer"
    )

    feedback = InterviewFeedback(
        interview_id=interview_id,
        technical_score=feedback_data.get("technical_score", 0),
        communication_score=feedback_data.get("communication_score", 0),
        confidence_score=feedback_data.get("confidence_score", 0),
        overall_rating=feedback_data.get("overall_rating", 0),
        improvement_suggestions=feedback_data.get("improvement_suggestions"),
        detailed_feedback=feedback_data.get("detailed_feedback"),
    )
    interview.status = "completed"
    interview.completed_at = datetime.utcnow()

    progress = LearningProgress(
        user_id=current_user.id,
        item_type="interview",
        title=f"Mock Interview: {interview.title}",
        status="completed",
        completed_at=datetime.utcnow(),
    )
    db.add(feedback)
    db.add(progress)
    db.commit()
    db.refresh(feedback)
    return feedback


@router.get("/{interview_id}/feedback", response_model=InterviewFeedbackResponse)
def get_feedback(
    interview_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    interview = (
        db.query(Interview)
        .filter(Interview.id == interview_id, Interview.user_id == current_user.id)
        .first()
    )
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    feedback = db.query(InterviewFeedback).filter(InterviewFeedback.interview_id == interview_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback

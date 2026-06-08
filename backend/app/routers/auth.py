from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.config import get_settings
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/dev-login")
def dev_login():
    settings = get_settings()
    if not settings.dev_mode:
        raise HTTPException(status_code=403, detail="Dev login is disabled")
    return {
        "token": settings.dev_auth_token,
        "message": "Use this token as Bearer token for API requests",
    }


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserResponse)
def update_me(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if data.display_name is not None:
        current_user.display_name = data.display_name
    if data.target_role is not None:
        current_user.target_role = data.target_role
    db.commit()
    db.refresh(current_user)
    return current_user

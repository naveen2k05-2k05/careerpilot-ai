from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.auth.firebase import verify_firebase_token
from app.config import get_settings
from app.database import get_db
from app.models.user import User
from app.seed_data import seed_demo_user_data

security = HTTPBearer()

DEV_FIREBASE_UID = "dev-local-user-001"
DEV_EMAIL = "demo@careerpilot.local"


def _get_or_create_dev_user(db: Session) -> User:
    user = db.query(User).filter(User.firebase_uid == DEV_FIREBASE_UID).first()
    if not user:
        user = User(
            firebase_uid=DEV_FIREBASE_UID,
            email=DEV_EMAIL,
            display_name="Demo User",
            target_role="Software Engineer",
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        seed_demo_user_data(db, user.id)
    return user


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    settings = get_settings()
    token = credentials.credentials

    if settings.dev_mode and token == settings.dev_auth_token:
        return _get_or_create_dev_user(db)

    decoded = verify_firebase_token(token)
    firebase_uid = decoded.get("uid")
    email = decoded.get("email", "")

    user = db.query(User).filter(User.firebase_uid == firebase_uid).first()
    if not user:
        user = User(
            firebase_uid=firebase_uid,
            email=email,
            display_name=decoded.get("name"),
            photo_url=decoded.get("picture"),
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return user


def get_optional_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db),
) -> User | None:
    if not credentials:
        return None
    try:
        return get_current_user(credentials, db)
    except HTTPException:
        return None

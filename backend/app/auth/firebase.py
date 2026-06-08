import json
import os
from functools import lru_cache

import firebase_admin
from firebase_admin import auth, credentials
from fastapi import HTTPException, status

from app.config import get_settings

_firebase_initialized = False


def init_firebase():
    global _firebase_initialized
    if _firebase_initialized:
        return

    settings = get_settings()
    cred_path = settings.firebase_credentials_path

    if cred_path and os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred, {"projectId": settings.firebase_project_id})
    elif os.environ.get("FIREBASE_CREDENTIALS_JSON"):
        cred_dict = json.loads(os.environ["FIREBASE_CREDENTIALS_JSON"])
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred, {"projectId": settings.firebase_project_id})
    else:
        try:
            firebase_admin.initialize_app(
                options={"projectId": settings.firebase_project_id} if settings.firebase_project_id else None
            )
        except Exception:
            pass

    _firebase_initialized = True


def verify_firebase_token(id_token: str) -> dict:
    init_firebase()
    try:
        decoded = auth.verify_id_token(id_token)
        return decoded
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication token: {str(e)}",
        )

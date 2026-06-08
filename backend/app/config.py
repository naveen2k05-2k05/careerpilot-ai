from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    database_url: str = "sqlite:///./careerpilot.db"
    firebase_project_id: str = ""
    firebase_credentials_path: str = "./firebase-credentials.json"
    gemini_api_key: str = ""
    cors_origins: str = (
    "http://localhost:5173,"
    "http://127.0.0.1:5173,"
    "https://pilotyourcareer.netlify.app"
    ) 

    secret_key: str = "dev-secret-key"
    dev_mode: bool = True
    dev_auth_token: str = "careerpilot-dev-local-token"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    return Settings()

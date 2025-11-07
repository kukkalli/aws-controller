from __future__ import annotations

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    APP_NAME: str = "aws-fastapi-starter"
    APP_ENV: str = "dev"
    LOG_LEVEL: str = "INFO"

    CORS_ALLOW_ORIGINS: List[str] = ["*"]

    AUTH_DISABLED: bool = True
    OIDC_ISSUER: str | None = None
    OIDC_AUDIENCE: str | None = None
    JWKS_JSON: str | None = None

    DB_URI: str = "sqlite+aiosqlite:///./data/app.db"

    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_REDIS_URL: str | None = None

settings = Settings()

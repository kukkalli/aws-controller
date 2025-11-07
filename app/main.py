from __future__ import annotations

import logging
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import init_logging
from app.core.security_headers import SecurityHeadersMiddleware
from app.core.rate_limit import RateLimitMiddleware
from app.api.v1 import health, users

init_logging(level=settings.LOG_LEVEL)

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
app.add_middleware(RateLimitMiddleware, requests_per_minute=settings.RATE_LIMIT_PER_MINUTE)

app.include_router(health.router, prefix="/v1")
app.include_router(users.router, prefix="/v1")

@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/readyz")
async def readyz() -> dict[str, str]:
    # TODO: Add deeper checks (DB, cache, etc.)
    return {"status": "ready"}

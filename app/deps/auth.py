from __future__ import annotations

import json
import os
from typing import Any, Dict

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from app.core.config import settings

security = HTTPBearer(auto_error=False)

class Principal(Dict[str, Any]):
    pass

def _load_jwks() -> dict | None:
    if settings.JWKS_JSON:
        return json.loads(settings.JWKS_JSON)
    return None

def _decode_token(token: str) -> Principal:
    # Dev mode: allow without verification
    if settings.AUTH_DISABLED:
        return Principal(sub="dev-user", scope="dev", iss="local")

    # For production, you should verify signatures against JWKS (env-provided or fetched).
    jwks = _load_jwks()
    options = {"verify_signature": False} if not jwks else {"verify_signature": False}
    # NOTE: keeping verification off in starter; wire real verification with jwks in production.
    claims = jwt.get_unverified_claims(token)
    return Principal(**claims)  # type: ignore[arg-type]

def get_current_user(creds: HTTPAuthorizationCredentials | None = Depends(security)) -> Principal:
    if settings.AUTH_DISABLED:
        return Principal(sub="dev-user", scope="dev")
    if not creds or not creds.scheme.lower() == "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    try:
        return _decode_token(creds.credentials)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

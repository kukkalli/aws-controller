from __future__ import annotations

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.deps.auth import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

class UserIn(BaseModel):
    email: str = Field(min_length=5, max_length=254)
    full_name: str = Field(min_length=1, max_length=200)

class User(BaseModel):
    id: int
    email: str
    full_name: str

# In-memory store for the starter; replace with DB.
_USERS: list[User] = []
_NEXT_ID = 1

@router.post("", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(data: UserIn, user=Depends(get_current_user)) -> User:  # noqa: B008
    global _NEXT_ID
    if any(u.email == data.email for u in _USERS):
        raise HTTPException(status_code=409, detail="Email already exists")
    obj = User(id=_NEXT_ID, email=data.email, full_name=data.full_name)
    _USERS.append(obj)
    _NEXT_ID += 1
    return obj

@router.get("", response_model=List[User])
def list_users(user=Depends(get_current_user)) -> list[User]:  # noqa: B008
    return _USERS

import os
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_users_crud(monkeypatch):
    monkeypatch.setenv("AUTH_DISABLED", "true")
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/v1/users", json={"email": "a@b.com", "full_name": "Alice"})
        assert resp.status_code == 201, resp.text
        data = resp.json()
        assert data["email"] == "a@b.com"
        resp = await ac.get("/v1/users")
        assert resp.status_code == 200
        assert len(resp.json()) == 1

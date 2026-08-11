from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest
from app.core.dependencies import get_db
from app.core.security import get_password_hash
from app.infrastructure.database.models.user import User
from app.main import app
from httpx import AsyncClient


async def override_get_db():
    yield None


app.dependency_overrides[get_db] = override_get_db


@pytest.mark.asyncio
async def test_login_success(async_client: AsyncClient):
    payload = {"username": "test@test.com", "password": "password123"}
    user_id = uuid4()
    mock_user = User(
        id=user_id,
        name="Test User",
        email="test@test.com",
        password_hash=get_password_hash("password123"),
        is_active=True,
        email_verified=False,
    )

    with patch("app.api.v1.auth.UserRepository") as MockRepo:
        mock_instance = MockRepo.return_value
        mock_instance.get_active_by_email = AsyncMock(return_value=mock_user)

        response = await async_client.post("/api/v1/auth/login", data=payload)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_failure(async_client: AsyncClient):
    payload = {"username": "test@test.com", "password": "wrongpassword"}
    user_id = uuid4()
    mock_user = User(
        id=user_id,
        name="Test User",
        email="test@test.com",
        password_hash=get_password_hash("password123"),
        is_active=True,
        email_verified=False,
    )

    with patch("app.api.v1.auth.UserRepository") as MockRepo:
        mock_instance = MockRepo.return_value
        mock_instance.get_active_by_email = AsyncMock(return_value=mock_user)

        response = await async_client.post("/api/v1/auth/login", data=payload)

        assert response.status_code == 401

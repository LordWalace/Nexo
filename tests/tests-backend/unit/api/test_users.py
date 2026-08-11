from datetime import UTC, datetime
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest
from app.core.dependencies import get_current_user, get_db
from app.infrastructure.database.models.user import User
from app.main import app
from httpx import AsyncClient


async def override_get_current_user():
    return User(
        id=uuid4(),
        name="Test User",
        email="test@test.com",
        is_active=True,
        email_verified=False,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )


async def override_get_db():
    yield None


app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db


@pytest.mark.asyncio
async def test_create_user_api(async_client: AsyncClient):
    payload = {"name": "Test User", "email": "test@test.com", "password": "password123"}
    user_id = uuid4()
    mock_user = User(
        id=user_id,
        name="Test User",
        email="test@test.com",
        is_active=True,
        email_verified=False,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    with patch("app.api.v1.users.UserUseCases") as MockUseCases:
        mock_instance = MockUseCases.return_value
        mock_instance.create_user = AsyncMock(return_value=mock_user)

        response = await async_client.post("/api/v1/users/", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test User"


@pytest.mark.asyncio
async def test_read_users_me_api(async_client: AsyncClient):
    response = await async_client.get("/api/v1/users/me")

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@test.com"

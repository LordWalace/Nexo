from datetime import UTC, datetime
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest
from app.core.dependencies import get_current_user, get_db
from app.infrastructure.database.models.category import Category
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
    )


async def override_get_db():
    yield None


app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db


@pytest.mark.asyncio
async def test_create_category_api(async_client: AsyncClient):
    payload = {"name": "Test Category"}
    user_id = uuid4()
    mock_category = Category(
        id=uuid4(),
        name="Test Category",
        user_id=user_id,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    with patch("app.api.v1.categories.CategoryUseCases") as MockUseCases:
        mock_instance = MockUseCases.return_value
        mock_instance.create_category = AsyncMock(return_value=mock_category)

        response = await async_client.post("/api/v1/categories/", json=payload)

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Category"


@pytest.mark.asyncio
async def test_get_categories_api(async_client: AsyncClient):
    user_id = uuid4()
    mock_category = Category(
        id=uuid4(),
        name="Test Category",
        user_id=user_id,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    with patch("app.api.v1.categories.CategoryUseCases") as MockUseCases:
        mock_instance = MockUseCases.return_value
        mock_instance.get_all_categories = AsyncMock(return_value=[mock_category])

        response = await async_client.get("/api/v1/categories/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Test Category"


@pytest.mark.asyncio
async def test_update_category_api(async_client: AsyncClient):
    payload = {"name": "Updated Category"}
    cat_id = str(uuid4())
    user_id = uuid4()
    mock_category = Category(
        id=cat_id,
        name="Updated Category",
        user_id=user_id,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    with patch("app.api.v1.categories.CategoryUseCases") as MockUseCases:
        mock_instance = MockUseCases.return_value
        mock_instance.update_category = AsyncMock(return_value=mock_category)

        response = await async_client.patch(
            f"/api/v1/categories/{cat_id}", json=payload
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Category"


@pytest.mark.asyncio
async def test_delete_category_api(async_client: AsyncClient):
    cat_id = str(uuid4())

    with patch("app.api.v1.categories.CategoryUseCases") as MockUseCases:
        mock_instance = MockUseCases.return_value
        mock_instance.delete_category = AsyncMock(return_value=None)

        response = await async_client.delete(f"/api/v1/categories/{cat_id}")

        assert response.status_code == 204

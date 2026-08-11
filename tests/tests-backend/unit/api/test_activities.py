import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock
from uuid import uuid4
from datetime import datetime, UTC

from app.main import app
from app.core.dependencies import get_current_user, get_db
from app.infrastructure.database.models.user import User
from app.infrastructure.database.models.activity import Activity

async def override_get_current_user():
    return User(id=uuid4(), name="Test User", email="test@test.com", is_active=True, email_verified=False)

async def override_get_db():
    yield None

app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db

@pytest.mark.asyncio
async def test_create_activity_api(async_client: AsyncClient):
    payload = {"title": "Test Activity", "category_id": str(uuid4())}
    user_id = uuid4()
    mock_activity = Activity(id=uuid4(), title="Test Activity", category_id=uuid4(), user_id=user_id, created_at=datetime.now(UTC), updated_at=datetime.now(UTC))
    
    with patch("app.api.v1.activities.ActivityUseCases") as MockUseCases:
        mock_instance = MockUseCases.return_value
        mock_instance.create_activity = AsyncMock(return_value=mock_activity)
        
        response = await async_client.post("/api/v1/activities/", json=payload)
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Activity"

@pytest.mark.asyncio
async def test_get_activities_api(async_client: AsyncClient):
    user_id = uuid4()
    mock_activity = Activity(id=uuid4(), title="Test Activity", category_id=uuid4(), user_id=user_id, created_at=datetime.now(UTC), updated_at=datetime.now(UTC))
    
    with patch("app.api.v1.activities.ActivityUseCases") as MockUseCases:
        mock_instance = MockUseCases.return_value
        mock_instance.get_all_activities = AsyncMock(return_value=[mock_activity])
        
        response = await async_client.get("/api/v1/activities/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Test Activity"

@pytest.mark.asyncio
async def test_update_activity_api(async_client: AsyncClient):
    payload = {"title": "Updated Activity"}
    act_id = str(uuid4())
    user_id = uuid4()
    mock_activity = Activity(id=act_id, title="Updated Activity", category_id=uuid4(), user_id=user_id, created_at=datetime.now(UTC), updated_at=datetime.now(UTC))
    
    with patch("app.api.v1.activities.ActivityUseCases") as MockUseCases:
        mock_instance = MockUseCases.return_value
        mock_instance.update_activity = AsyncMock(return_value=mock_activity)
        
        response = await async_client.patch(f"/api/v1/activities/{act_id}", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Activity"

@pytest.mark.asyncio
async def test_delete_activity_api(async_client: AsyncClient):
    act_id = str(uuid4())
    
    with patch("app.api.v1.activities.ActivityUseCases") as MockUseCases:
        mock_instance = MockUseCases.return_value
        mock_instance.delete_activity = AsyncMock(return_value=None)
        
        response = await async_client.delete(f"/api/v1/activities/{act_id}")
        
        assert response.status_code == 204

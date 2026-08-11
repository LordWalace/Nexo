import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock
from uuid import uuid4
from datetime import datetime, UTC

from app.main import app
from app.core.dependencies import get_current_user, get_db
from app.infrastructure.database.models.user import User
from app.infrastructure.database.models.execution_period import ActivityExecutionPeriod

async def override_get_current_user():
    return User(id=uuid4(), name="Test User", email="test@test.com", is_active=True, email_verified=False)

async def override_get_db():
    yield None

app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db

@pytest.mark.asyncio
async def test_create_history_api(async_client: AsyncClient):
    payload = {"activity_id": str(uuid4()), "start_time": datetime.now(UTC).isoformat()}
    user_id = uuid4()
    mock_history = ActivityExecutionPeriod(id=uuid4(), activity_id=uuid4(), user_id=user_id, start_time=datetime.now(UTC), created_at=datetime.now(UTC), updated_at=datetime.now(UTC))
    
    with patch("app.api.v1.history.HistoryUseCases") as MockUseCases:
        mock_instance = MockUseCases.return_value
        mock_instance.create_history = AsyncMock(return_value=mock_history)
        
        response = await async_client.post("/api/v1/history/", json=payload)
        
        assert response.status_code == 201
        data = response.json()
        assert "id" in data

@pytest.mark.asyncio
async def test_get_history_api(async_client: AsyncClient):
    user_id = uuid4()
    mock_history = ActivityExecutionPeriod(id=uuid4(), activity_id=uuid4(), user_id=user_id, start_time=datetime.now(UTC), created_at=datetime.now(UTC), updated_at=datetime.now(UTC))
    
    with patch("app.api.v1.history.HistoryUseCases") as MockUseCases:
        mock_instance = MockUseCases.return_value
        mock_instance.get_all_history = AsyncMock(return_value=[mock_history])
        
        response = await async_client.get("/api/v1/history/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

@pytest.mark.asyncio
async def test_update_history_api(async_client: AsyncClient):
    payload = {"end_time": datetime.now(UTC).isoformat()}
    period_id = str(uuid4())
    user_id = uuid4()
    mock_history = ActivityExecutionPeriod(id=period_id, activity_id=uuid4(), user_id=user_id, start_time=datetime.now(UTC), end_time=datetime.now(UTC), created_at=datetime.now(UTC), updated_at=datetime.now(UTC))
    
    with patch("app.api.v1.history.HistoryUseCases") as MockUseCases:
        mock_instance = MockUseCases.return_value
        mock_instance.update_history = AsyncMock(return_value=mock_history)
        
        response = await async_client.patch(f"/api/v1/history/{period_id}", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert data["end_time"] is not None

@pytest.mark.asyncio
async def test_delete_history_api(async_client: AsyncClient):
    period_id = str(uuid4())
    
    with patch("app.api.v1.history.HistoryUseCases") as MockUseCases:
        mock_instance = MockUseCases.return_value
        mock_instance.delete_history = AsyncMock(return_value=None)
        
        response = await async_client.delete(f"/api/v1/history/{period_id}")
        
        assert response.status_code == 204

import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock
from uuid import uuid4
from datetime import datetime, UTC

from app.main import app
from app.core.dependencies import get_current_user, get_db
from app.infrastructure.database.models.user import User
from app.infrastructure.database.models.notification import Notification

async def override_get_current_user():
    return User(id=uuid4(), name="Test User", email="test@test.com", is_active=True, email_verified=False)

async def override_get_db():
    yield None

app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db

@pytest.mark.asyncio
async def test_create_notification_api(async_client: AsyncClient):
    payload = {"title": "Test Notification", "message": "Test"}
    user_id = uuid4()
    mock_notification = Notification(id=uuid4(), title="Test Notification", message="Test", is_read=False, user_id=user_id, created_at=datetime.now(UTC))
    
    with patch("app.api.v1.notifications.NotificationUseCases") as MockUseCases:
        mock_instance = MockUseCases.return_value
        mock_instance.create_notification = AsyncMock(return_value=mock_notification)
        
        response = await async_client.post("/api/v1/notifications/", json=payload)
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Notification"

@pytest.mark.asyncio
async def test_get_notifications_api(async_client: AsyncClient):
    user_id = uuid4()
    mock_notification = Notification(id=uuid4(), title="Test Notification", message="Test", is_read=False, user_id=user_id, created_at=datetime.now(UTC))
    
    with patch("app.api.v1.notifications.NotificationUseCases") as MockUseCases:
        mock_instance = MockUseCases.return_value
        mock_instance.get_all_notifications = AsyncMock(return_value=[mock_notification])
        
        response = await async_client.get("/api/v1/notifications/")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Test Notification"

@pytest.mark.asyncio
async def test_mark_notification_as_read_api(async_client: AsyncClient):
    notif_id = str(uuid4())
    user_id = uuid4()
    mock_notification = Notification(id=notif_id, title="Test Notification", message="Test", is_read=True, user_id=user_id, created_at=datetime.now(UTC))
    
    with patch("app.api.v1.notifications.NotificationUseCases") as MockUseCases:
        mock_instance = MockUseCases.return_value
        mock_instance.mark_as_read = AsyncMock(return_value=mock_notification)
        
        response = await async_client.patch(f"/api/v1/notifications/{notif_id}/read")
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_read"] is True

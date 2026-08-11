import pytest
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock
from uuid import uuid4

from app.main import app
from app.core.dependencies import get_current_user, get_db
from app.infrastructure.database.models.user import User
from app.schemas.statistics import StatisticsResponse

async def override_get_current_user():
    return User(id=uuid4(), name="Test User", email="test@test.com", is_active=True, email_verified=False)

async def override_get_db():
    yield None

app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db

@pytest.mark.asyncio
async def test_get_statistics_api(async_client: AsyncClient):
    mock_stats = StatisticsResponse(total_activities=10, total_execution_periods=5)
    
    with patch("app.api.v1.statistics.StatisticsUseCases") as MockUseCases:
        mock_instance = MockUseCases.return_value
        mock_instance.get_user_statistics = AsyncMock(return_value=mock_stats)
        
        response = await async_client.get("/api/v1/statistics/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_activities"] == 10
        assert data["total_execution_periods"] == 5

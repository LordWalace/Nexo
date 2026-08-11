import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock

from app.main import app
from app.core.dependencies import get_db
from app.core.redis import get_redis

async def mock_get_db_success():
    mock_session = AsyncMock()
    mock_session.execute = AsyncMock()
    yield mock_session

async def mock_get_db_failure():
    mock_session = AsyncMock()
    mock_session.execute.side_effect = Exception("DB Error")
    yield mock_session

async def mock_get_redis_success():
    mock_redis = AsyncMock()
    mock_redis.ping = AsyncMock()
    yield mock_redis
    
async def mock_get_redis_failure():
    mock_redis = AsyncMock()
    mock_redis.ping.side_effect = Exception("Redis Error")
    yield mock_redis

@pytest.mark.asyncio
async def test_health_check(async_client: AsyncClient):
    response = await async_client.get("/api/v1/health")
    # Health endpoint without trailing slash redirects, or not.
    # Wait, the route is @router.get(""). In app.main, router is included with prefix="/health".
    # So "/api/v1/health" or "/api/v1/health/" could be it.
    if response.status_code == 307:
        response = await async_client.get("/api/v1/health/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

@pytest.mark.asyncio
async def test_health_check_database_success(async_client: AsyncClient):
    app.dependency_overrides[get_db] = mock_get_db_success
    response = await async_client.get("/api/v1/health/database")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    app.dependency_overrides.pop(get_db, None)
    app.dependency_overrides.pop(get_redis, None)

@pytest.mark.asyncio
async def test_health_check_database_failure(async_client: AsyncClient):
    app.dependency_overrides[get_db] = mock_get_db_failure
    response = await async_client.get("/api/v1/health/database")
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "DATABASE_UNAVAILABLE"
    app.dependency_overrides.pop(get_db, None)
    app.dependency_overrides.pop(get_redis, None)

@pytest.mark.asyncio
async def test_health_check_redis_success(async_client: AsyncClient):
    app.dependency_overrides[get_redis] = mock_get_redis_success
    response = await async_client.get("/api/v1/health/redis")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    app.dependency_overrides.pop(get_db, None)
    app.dependency_overrides.pop(get_redis, None)

@pytest.mark.asyncio
async def test_health_check_redis_failure(async_client: AsyncClient):
    app.dependency_overrides[get_redis] = mock_get_redis_failure
    response = await async_client.get("/api/v1/health/redis")
    assert response.status_code == 503
    assert response.json()["error"]["code"] == "REDIS_UNAVAILABLE"
    app.dependency_overrides.pop(get_db, None)
    app.dependency_overrides.pop(get_redis, None)

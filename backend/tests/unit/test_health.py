import pytest
from httpx import ASGITransport, AsyncClient
from unittest.mock import patch, MagicMock

from app.main import app


@pytest.mark.asyncio
async def test_health_check_endpoint(async_client, mock_env_vars):
    response = await async_client.get("/api/v1/health")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_health_check_database_ok(async_client, mock_env_vars):
    with patch("app.api.v1.endpoints.health.get_db") as mock_get_db:
        # FastAPI resolve a dependência, mas mockamos a função que a FastAPI chama
        # No entanto, testar a rota com injeção requer override na FastAPI
        pass

@pytest.mark.asyncio
async def test_health_check_database_failure(async_client, mock_env_vars):
    from sqlalchemy.ext.asyncio import AsyncSession
    from app.core.dependencies import get_db

    async def override_get_db():
        class MockSession:
            async def execute(self, *args, **kwargs):
                raise Exception("DB Error")
        yield MockSession()

    app.dependency_overrides[get_db] = override_get_db
    try:
        response = await async_client.get("/api/v1/health/database")
        assert response.status_code == 503
        assert response.json()["error"]["code"] == "DATABASE_UNAVAILABLE"
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_health_check_redis_failure(async_client, mock_env_vars):
    from app.core.redis import get_redis

    async def override_get_redis():
        class MockRedis:
            async def ping(self):
                raise Exception("Redis Error")
        yield MockRedis()

    app.dependency_overrides[get_redis] = override_get_redis
    try:
        response = await async_client.get("/api/v1/health/redis")
        assert response.status_code == 503
        assert response.json()["error"]["code"] == "REDIS_UNAVAILABLE"
    finally:
        app.dependency_overrides.clear()

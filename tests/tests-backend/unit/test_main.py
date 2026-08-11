import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app

@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to Nexo API", "docs": "/docs"}

@pytest.mark.asyncio
async def test_lifespan():
    # Test lifespan startup and shutdown
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ):
        pass # Lifespan startup and shutdown are executed

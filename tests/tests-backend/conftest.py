import asyncio
import os
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

os.environ["DATABASE_URL"] = (
    "postgresql+asyncpg://postgres:postgres@127.0.0.1:5433/nexo_db"
)
os.environ["REDIS_URL"] = "redis://localhost:6379/0"
os.environ["JWT_SECRET_KEY"] = (
    "testsecret_must_be_32_bytes_long_for_security_algorithms"
)
os.environ["STORAGE_ENDPOINT"] = "http://localhost:9000"
os.environ["STORAGE_ACCESS_KEY"] = "test"
os.environ["STORAGE_SECRET_KEY"] = "test"
os.environ["STORAGE_BUCKET"] = "test"
os.environ["APP_SLUG"] = "nexo"

from collections.abc import AsyncGenerator

import pytest
from app.infrastructure.database.session import AsyncSessionLocal
from app.main import app
from httpx import ASGITransport, AsyncClient


@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Seta as variáveis de ambiente necessárias para testes unitários isolados (já setadas no escopo do módulo para import)."""
    monkeypatch.setenv("DATABASE_URL", os.environ["DATABASE_URL"])
    monkeypatch.setenv("JWT_SECRET_KEY", os.environ["JWT_SECRET_KEY"])


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Cliente HTTP para testes de integração de API."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest.fixture
async def db_session() -> AsyncGenerator:
    """Sessão de banco de dados para testes de integração. Executa rollback ao final."""
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()

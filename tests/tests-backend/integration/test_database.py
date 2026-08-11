import uuid
import pytest
from sqlalchemy import text

from app.core.security import get_password_hash
from app.infrastructure.database.models.user import User

pytestmark = pytest.mark.integration

@pytest.mark.asyncio
async def test_database_connection(db_session):
    try:
        result = await db_session.execute(text("SELECT 1"))
        assert result.scalar() == 1
    except Exception as e:
        pytest.fail(f"Dependência ausente: O serviço do banco de dados (PostgreSQL) não está disponível. Detalhes: {e}")

@pytest.mark.asyncio
async def test_create_user(db_session):
    new_user = User(
        id=uuid.uuid4(),
        name="Integration Test",
        email=f"test_{uuid.uuid4()}@nexo.test",
        password_hash=get_password_hash("123456"),
    )
    db_session.add(new_user)
    try:
        await db_session.commit()
        assert new_user.id is not None
    except Exception as e:
        pytest.fail(f"Dependência ausente: O serviço do banco de dados (PostgreSQL) não está disponível. Detalhes: {e}")

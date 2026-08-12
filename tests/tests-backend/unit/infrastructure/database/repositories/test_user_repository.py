from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from app.infrastructure.database.models.user import User
from app.infrastructure.database.repositories.user_repository import UserRepository


@pytest.mark.asyncio
async def test_create_user():
    session_mock = AsyncMock()
    repo = UserRepository(session=session_mock)

    user = User(
        id=uuid4(), name="Test User", email="test@test.com", password_hash="hash"
    )
    result = await repo.create(user)

    session_mock.add.assert_called_once_with(user)
    assert result == user


@pytest.mark.asyncio
async def test_get_by_id_user():
    session_mock = AsyncMock()
    repo = UserRepository(session=session_mock)

    user_id = uuid4()
    mock_result = MagicMock()
    user = User(
        id=user_id, name="Test User", email="test@test.com", password_hash="hash"
    )
    mock_result.scalar_one_or_none.return_value = user
    session_mock.execute.return_value = mock_result

    result = await repo.get_by_id(user_id)

    session_mock.execute.assert_awaited_once()
    assert result == user


@pytest.mark.asyncio
async def test_get_by_email():
    session_mock = AsyncMock()
    repo = UserRepository(session=session_mock)

    mock_result = MagicMock()
    user = User(
        id=uuid4(), name="Test User", email="test@test.com", password_hash="hash"
    )
    mock_result.scalar_one_or_none.return_value = user
    session_mock.execute.return_value = mock_result

    result = await repo.get_by_email("test@test.com")

    session_mock.execute.assert_awaited_once()
    assert result == user


@pytest.mark.asyncio
async def test_get_active_by_email():
    session_mock = AsyncMock()
    repo = UserRepository(session=session_mock)

    mock_result = MagicMock()
    user = User(
        id=uuid4(), name="Test User", email="test@test.com", password_hash="hash"
    )
    mock_result.scalar_one_or_none.return_value = user
    session_mock.execute.return_value = mock_result

    result = await repo.get_active_by_email("test@test.com")

    session_mock.execute.assert_awaited_once()
    assert result == user


@pytest.mark.asyncio
async def test_exists_by_email():
    session_mock = AsyncMock()
    repo = UserRepository(session=session_mock)

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = uuid4()
    session_mock.execute.return_value = mock_result

    result = await repo.exists_by_email("test@test.com")

    session_mock.execute.assert_awaited_once()
    assert result is True


@pytest.mark.asyncio
async def test_update_user():
    session_mock = AsyncMock()
    repo = UserRepository(session=session_mock)

    user = User(id=uuid4(), name="Updated", email="test@test.com", password_hash="hash")
    result = await repo.update(user)

    session_mock.add.assert_called_once_with(user)
    assert result == user


@pytest.mark.asyncio
async def test_soft_delete_user():
    session_mock = AsyncMock()
    repo = UserRepository(session=session_mock)

    user = User(id=uuid4(), name="Test", email="test@test.com", password_hash="hash")
    assert user.deleted_at is None

    result = await repo.soft_delete(user)

    assert result.deleted_at is not None
    session_mock.add.assert_called_once_with(user)
    assert result == user


@pytest.mark.asyncio
async def test_restore_user():
    session_mock = AsyncMock()
    repo = UserRepository(session=session_mock)

    user = User(
        id=uuid4(),
        name="Test",
        email="test@test.com",
        password_hash="hash",
        deleted_at=datetime.now(UTC),
    )
    assert user.deleted_at is not None

    result = await repo.restore(user)

    assert result.deleted_at is None
    session_mock.add.assert_called_once_with(user)
    assert result == user

from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest
from app.core.dependencies import get_current_user, get_db
from app.core.exceptions import AppException
from app.infrastructure.database.models.user import User


@pytest.mark.asyncio
async def test_get_db():
    # Since get_db is an async generator testing it directly can be done via manual __anext__
    # However we can just test that it yields an AsyncSession mock.
    with patch("app.core.dependencies.AsyncSessionLocal") as mock_session_local:
        mock_session = AsyncMock()
        mock_session_local.return_value.__aenter__.return_value = mock_session

        db_generator = get_db()
        session = await db_generator.__anext__()

        assert session == mock_session

        # Test the finally block closing the session
        try:
            await db_generator.__anext__()
        except StopAsyncIteration:
            pass

        mock_session.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_current_user_valid():
    token = "valid_token"
    user_id = uuid4()
    mock_session = AsyncMock()

    mock_user = User(id=user_id, is_active=True, deleted_at=None)

    with (
        patch(
            "app.core.dependencies.decode_access_token", return_value=str(user_id)
        ) as mock_decode,
        patch("app.core.dependencies.UserRepository") as mock_repo_class,
    ):
        mock_repo = AsyncMock()
        mock_repo.get_by_id.return_value = mock_user
        mock_repo_class.return_value = mock_repo

        result = await get_current_user(token=token, session=mock_session)

        assert result == mock_user
        mock_decode.assert_called_once_with(token)
        mock_repo_class.assert_called_once_with(mock_session)
        mock_repo.get_by_id.assert_awaited_once_with(user_id)


@pytest.mark.asyncio
async def test_get_current_user_invalid_subject_uuid():
    token = "valid_token_but_bad_subject"
    mock_session = AsyncMock()

    with patch("app.core.dependencies.decode_access_token", return_value="not-a-uuid"):
        with pytest.raises(AppException) as excinfo:
            await get_current_user(token=token, session=mock_session)

        assert excinfo.value.code == "TOKEN_INVALID_SUBJECT"


@pytest.mark.asyncio
async def test_get_current_user_not_found():
    token = "valid_token"
    user_id = uuid4()
    mock_session = AsyncMock()

    with (
        patch("app.core.dependencies.decode_access_token", return_value=str(user_id)),
        patch("app.core.dependencies.UserRepository") as mock_repo_class,
    ):
        mock_repo = AsyncMock()
        mock_repo.get_by_id.return_value = None
        mock_repo_class.return_value = mock_repo

        with pytest.raises(AppException) as excinfo:
            await get_current_user(token=token, session=mock_session)

        assert excinfo.value.code == "USER_NOT_FOUND_OR_INACTIVE"


@pytest.mark.asyncio
async def test_get_current_user_inactive():
    token = "valid_token"
    user_id = uuid4()
    mock_session = AsyncMock()

    mock_user = User(id=user_id, is_active=False, deleted_at=None)

    with (
        patch("app.core.dependencies.decode_access_token", return_value=str(user_id)),
        patch("app.core.dependencies.UserRepository") as mock_repo_class,
    ):
        mock_repo = AsyncMock()
        mock_repo.get_by_id.return_value = mock_user
        mock_repo_class.return_value = mock_repo

        with pytest.raises(AppException) as excinfo:
            await get_current_user(token=token, session=mock_session)

        assert excinfo.value.code == "USER_NOT_FOUND_OR_INACTIVE"


@pytest.mark.asyncio
async def test_get_current_user_deleted():
    token = "valid_token"
    user_id = uuid4()
    mock_session = AsyncMock()

    from datetime import UTC, datetime

    mock_user = User(id=user_id, is_active=True, deleted_at=datetime.now(UTC))

    with (
        patch("app.core.dependencies.decode_access_token", return_value=str(user_id)),
        patch("app.core.dependencies.UserRepository") as mock_repo_class,
    ):
        mock_repo = AsyncMock()
        mock_repo.get_by_id.return_value = mock_user
        mock_repo_class.return_value = mock_repo

        with pytest.raises(AppException) as excinfo:
            await get_current_user(token=token, session=mock_session)

        assert excinfo.value.code == "USER_NOT_FOUND_OR_INACTIVE"

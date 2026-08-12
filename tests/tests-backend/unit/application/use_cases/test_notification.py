from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from app.application.use_cases.notification import NotificationUseCases
from app.core.exceptions import AppException
from app.infrastructure.database.models.notification import Notification
from app.schemas.notification import NotificationCreate


@pytest.mark.asyncio
async def test_create_notification():
    mock_repo = AsyncMock()
    mock_session = AsyncMock()

    use_cases = NotificationUseCases(repository=mock_repo, session=mock_session)
    user_id = uuid4()
    notif_in = NotificationCreate(title="Alerta", message="Teste")

    result = await use_cases.create_notification(
        user_id=user_id, notification_in=notif_in
    )

    mock_repo.create.assert_awaited_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()
    assert result.title == "Alerta"
    assert result.message == "Teste"
    assert result.user_id == user_id


@pytest.mark.asyncio
async def test_get_all_notifications():
    mock_repo = AsyncMock()
    mock_session = AsyncMock()

    use_cases = NotificationUseCases(repository=mock_repo, session=mock_session)
    user_id = uuid4()

    expected_list = [
        Notification(id=uuid4(), title="Not1", message="Teste", user_id=user_id)
    ]
    mock_repo.get_all_by_user.return_value = expected_list

    result = await use_cases.get_all_notifications(user_id=user_id)

    mock_repo.get_all_by_user.assert_awaited_once_with(user_id)
    assert result == expected_list


@pytest.mark.asyncio
async def test_mark_as_read_success():
    mock_repo = AsyncMock()
    mock_session = AsyncMock()

    use_cases = NotificationUseCases(repository=mock_repo, session=mock_session)
    user_id = uuid4()
    notif_id = uuid4()

    existing_notif = Notification(
        id=notif_id, title="Not1", message="Teste", user_id=user_id, is_read=False
    )
    mock_repo.get_by_id.return_value = existing_notif

    result = await use_cases.mark_as_read(notification_id=notif_id, user_id=user_id)

    mock_repo.get_by_id.assert_awaited_once_with(notif_id, user_id)
    mock_repo.update.assert_awaited_once_with(existing_notif)
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()
    assert result.is_read is True


@pytest.mark.asyncio
async def test_mark_as_read_not_found():
    mock_repo = AsyncMock()
    mock_session = AsyncMock()

    use_cases = NotificationUseCases(repository=mock_repo, session=mock_session)
    user_id = uuid4()
    notif_id = uuid4()

    mock_repo.get_by_id.return_value = None

    with pytest.raises(AppException) as excinfo:
        await use_cases.mark_as_read(notification_id=notif_id, user_id=user_id)

    assert excinfo.value.code == "NOTIFICATION_NOT_FOUND"

from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from app.infrastructure.database.models.notification import Notification
from app.infrastructure.database.repositories.notification_repository import (
    NotificationRepository,
)


@pytest.mark.asyncio
async def test_create_notification():
    session_mock = AsyncMock()
    repo = NotificationRepository(session=session_mock)

    notification = Notification(
        id=uuid4(), title="Alerta", message="Teste", user_id=uuid4()
    )
    result = await repo.create(notification)

    session_mock.add.assert_called_once_with(notification)
    assert result == notification


@pytest.mark.asyncio
async def test_get_by_id_notification():
    session_mock = AsyncMock()
    repo = NotificationRepository(session=session_mock)

    notif_id = uuid4()
    user_id = uuid4()

    mock_result = MagicMock()
    mock_scalars = MagicMock()

    notification = Notification(
        id=notif_id, title="Alerta", message="Teste", user_id=user_id
    )
    mock_scalars.first.return_value = notification
    mock_result.scalars.return_value = mock_scalars

    session_mock.execute.return_value = mock_result

    result = await repo.get_by_id(notif_id, user_id)

    session_mock.execute.assert_awaited_once()
    assert result == notification


@pytest.mark.asyncio
async def test_get_all_by_user_notification():
    session_mock = AsyncMock()
    repo = NotificationRepository(session=session_mock)

    user_id = uuid4()

    mock_result = MagicMock()
    mock_scalars = MagicMock()

    notification_list = [
        Notification(id=uuid4(), title="Alerta 1", message="Teste 1", user_id=user_id),
        Notification(id=uuid4(), title="Alerta 2", message="Teste 2", user_id=user_id),
    ]
    mock_scalars.all.return_value = notification_list
    mock_result.scalars.return_value = mock_scalars

    session_mock.execute.return_value = mock_result

    result = await repo.get_all_by_user(user_id)

    session_mock.execute.assert_awaited_once()
    assert result == notification_list


@pytest.mark.asyncio
async def test_update_notification():
    session_mock = AsyncMock()
    repo = NotificationRepository(session=session_mock)

    notification = Notification(
        id=uuid4(), title="Alerta Update", message="Teste Update", user_id=uuid4()
    )
    result = await repo.update(notification)

    assert result == notification

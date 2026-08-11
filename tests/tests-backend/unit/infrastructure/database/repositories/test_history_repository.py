from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from app.infrastructure.database.models.execution_period import ActivityExecutionPeriod
from app.infrastructure.database.repositories.history_repository import (
    HistoryRepository,
)


@pytest.mark.asyncio
async def test_create_history():
    session_mock = AsyncMock()
    repo = HistoryRepository(session=session_mock)

    period = ActivityExecutionPeriod(
        id=uuid4(), start_time=datetime.now(UTC), user_id=uuid4(), activity_id=uuid4()
    )
    result = await repo.create(period)

    session_mock.add.assert_called_once_with(period)
    assert result == period


@pytest.mark.asyncio
async def test_get_by_id_history():
    session_mock = AsyncMock()
    repo = HistoryRepository(session=session_mock)

    period_id = uuid4()
    user_id = uuid4()

    mock_result = MagicMock()
    mock_scalars = MagicMock()

    period = ActivityExecutionPeriod(
        id=period_id, start_time=datetime.now(UTC), user_id=user_id, activity_id=uuid4()
    )
    mock_scalars.first.return_value = period
    mock_result.scalars.return_value = mock_scalars

    session_mock.execute.return_value = mock_result

    result = await repo.get_by_id(period_id, user_id)

    session_mock.execute.assert_awaited_once()
    assert result == period


@pytest.mark.asyncio
async def test_get_all_by_user_history():
    session_mock = AsyncMock()
    repo = HistoryRepository(session=session_mock)

    user_id = uuid4()

    mock_result = MagicMock()
    mock_scalars = MagicMock()

    period_list = [
        ActivityExecutionPeriod(
            id=uuid4(),
            start_time=datetime.now(UTC),
            user_id=user_id,
            activity_id=uuid4(),
        ),
        ActivityExecutionPeriod(
            id=uuid4(),
            start_time=datetime.now(UTC),
            user_id=user_id,
            activity_id=uuid4(),
        ),
    ]
    mock_scalars.all.return_value = period_list
    mock_result.scalars.return_value = mock_scalars

    session_mock.execute.return_value = mock_result

    result = await repo.get_all_by_user(user_id)

    session_mock.execute.assert_awaited_once()
    assert result == period_list


@pytest.mark.asyncio
async def test_update_history():
    session_mock = AsyncMock()
    repo = HistoryRepository(session=session_mock)

    period = ActivityExecutionPeriod(
        id=uuid4(), start_time=datetime.now(UTC), user_id=uuid4(), activity_id=uuid4()
    )
    result = await repo.update(period)

    assert result == period


@pytest.mark.asyncio
async def test_delete_history():
    session_mock = AsyncMock()
    repo = HistoryRepository(session=session_mock)

    period = ActivityExecutionPeriod(
        id=uuid4(), start_time=datetime.now(UTC), user_id=uuid4(), activity_id=uuid4()
    )

    await repo.delete(period)

    session_mock.delete.assert_awaited_once_with(period)

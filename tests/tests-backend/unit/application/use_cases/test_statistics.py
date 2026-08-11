from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from app.application.use_cases.statistics import StatisticsUseCases


@pytest.mark.asyncio
async def test_get_user_statistics():
    mock_activity_repo = AsyncMock()
    mock_history_repo = AsyncMock()
    mock_session = AsyncMock()

    use_cases = StatisticsUseCases(
        activity_repo=mock_activity_repo,
        history_repo=mock_history_repo,
        session=mock_session,
    )
    user_id = uuid4()

    mock_activity_repo.get_all_by_user.return_value = ["act1", "act2", "act3"]
    mock_history_repo.get_all_by_user.return_value = ["hist1", "hist2"]

    result = await use_cases.get_user_statistics(user_id=user_id)

    mock_activity_repo.get_all_by_user.assert_awaited_once_with(user_id)
    mock_history_repo.get_all_by_user.assert_awaited_once_with(user_id)

    assert result.total_activities == 3
    assert result.total_execution_periods == 2

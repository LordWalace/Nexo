import pytest
from unittest.mock import AsyncMock
from uuid import uuid4
from datetime import datetime, UTC

from app.application.use_cases.history import HistoryUseCases
from app.infrastructure.database.models.execution_period import ActivityExecutionPeriod
from app.schemas.history import HistoryCreate, HistoryUpdate
from app.core.exceptions import AppException

@pytest.mark.asyncio
async def test_create_history():
    mock_repo = AsyncMock()
    mock_session = AsyncMock()
    
    use_cases = HistoryUseCases(repository=mock_repo, session=mock_session)
    user_id = uuid4()
    act_id = uuid4()
    start_time = datetime.now(UTC)
    history_in = HistoryCreate(activity_id=act_id, start_time=start_time)
    
    result = await use_cases.create_history(user_id=user_id, history_in=history_in)
    
    mock_repo.create.assert_awaited_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()
    assert result.activity_id == act_id
    assert result.start_time == start_time
    assert result.user_id == user_id

@pytest.mark.asyncio
async def test_get_all_history():
    mock_repo = AsyncMock()
    mock_session = AsyncMock()
    
    use_cases = HistoryUseCases(repository=mock_repo, session=mock_session)
    user_id = uuid4()
    
    expected_list = [ActivityExecutionPeriod(id=uuid4(), start_time=datetime.now(UTC), user_id=user_id, activity_id=uuid4())]
    mock_repo.get_all_by_user.return_value = expected_list
    
    result = await use_cases.get_all_history(user_id=user_id)
    
    mock_repo.get_all_by_user.assert_awaited_once_with(user_id)
    assert result == expected_list

@pytest.mark.asyncio
async def test_update_history_success():
    mock_repo = AsyncMock()
    mock_session = AsyncMock()
    
    use_cases = HistoryUseCases(repository=mock_repo, session=mock_session)
    user_id = uuid4()
    period_id = uuid4()
    
    existing_period = ActivityExecutionPeriod(id=period_id, start_time=datetime.now(UTC), user_id=user_id, activity_id=uuid4())
    mock_repo.get_by_id.return_value = existing_period
    
    new_end_time = datetime.now(UTC)
    update_data = HistoryUpdate(end_time=new_end_time)
    
    result = await use_cases.update_history(period_id=period_id, user_id=user_id, history_in=update_data)
    
    mock_repo.get_by_id.assert_awaited_once_with(period_id, user_id)
    mock_repo.update.assert_awaited_once_with(existing_period)
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()
    assert result.end_time == new_end_time

@pytest.mark.asyncio
async def test_update_history_start_time():
    mock_repo = AsyncMock()
    mock_session = AsyncMock()
    
    use_cases = HistoryUseCases(repository=mock_repo, session=mock_session)
    user_id = uuid4()
    period_id = uuid4()
    
    start_time = datetime.now(UTC)
    existing_period = ActivityExecutionPeriod(id=period_id, start_time=start_time, user_id=user_id, activity_id=uuid4())
    mock_repo.get_by_id.return_value = existing_period
    
    from datetime import timedelta
    new_start_time = start_time - timedelta(days=1)
    update_data = HistoryUpdate(start_time=new_start_time)
    
    result = await use_cases.update_history(period_id=period_id, user_id=user_id, history_in=update_data)
        
    assert result.start_time == new_start_time

@pytest.mark.asyncio
async def test_update_history_not_found():
    mock_repo = AsyncMock()
    mock_session = AsyncMock()
    
    use_cases = HistoryUseCases(repository=mock_repo, session=mock_session)
    user_id = uuid4()
    period_id = uuid4()
    
    mock_repo.get_by_id.return_value = None
    update_data = HistoryUpdate(end_time=datetime.now(UTC))
    
    with pytest.raises(AppException) as excinfo:
        await use_cases.update_history(period_id=period_id, user_id=user_id, history_in=update_data)
        
    assert excinfo.value.code == "HISTORY_NOT_FOUND"

@pytest.mark.asyncio
async def test_delete_history_success():
    mock_repo = AsyncMock()
    mock_session = AsyncMock()
    
    use_cases = HistoryUseCases(repository=mock_repo, session=mock_session)
    user_id = uuid4()
    period_id = uuid4()
    
    existing_period = ActivityExecutionPeriod(id=period_id, start_time=datetime.now(UTC), user_id=user_id, activity_id=uuid4())
    mock_repo.get_by_id.return_value = existing_period
    
    await use_cases.delete_history(period_id=period_id, user_id=user_id)
    
    mock_repo.delete.assert_awaited_once_with(existing_period)
    mock_session.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_delete_history_not_found():
    mock_repo = AsyncMock()
    mock_session = AsyncMock()
    
    use_cases = HistoryUseCases(repository=mock_repo, session=mock_session)
    user_id = uuid4()
    period_id = uuid4()
    
    mock_repo.get_by_id.return_value = None
    
    with pytest.raises(AppException) as excinfo:
        await use_cases.delete_history(period_id=period_id, user_id=user_id)
        
    assert excinfo.value.code == "HISTORY_NOT_FOUND"

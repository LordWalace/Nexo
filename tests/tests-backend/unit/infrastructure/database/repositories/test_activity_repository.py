import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from datetime import datetime, UTC

from app.infrastructure.database.models.activity import Activity
from app.infrastructure.database.repositories.activity_repository import ActivityRepository

@pytest.mark.asyncio
async def test_create_activity():
    session_mock = AsyncMock()
    repo = ActivityRepository(session=session_mock)
    
    activity = Activity(id=uuid4(), title="Estudar Matemática", user_id=uuid4())
    result = await repo.create(activity)
    
    session_mock.add.assert_called_once_with(activity)
    assert result == activity

@pytest.mark.asyncio
async def test_get_by_id_activity():
    session_mock = AsyncMock()
    repo = ActivityRepository(session=session_mock)
    
    act_id = uuid4()
    user_id = uuid4()
    
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    
    activity = Activity(id=act_id, title="Estudar", user_id=user_id)
    mock_scalars.first.return_value = activity
    mock_result.scalars.return_value = mock_scalars
    
    session_mock.execute.return_value = mock_result
    
    result = await repo.get_by_id(act_id, user_id)
    
    session_mock.execute.assert_awaited_once()
    assert result == activity

@pytest.mark.asyncio
async def test_get_all_by_user_activity():
    session_mock = AsyncMock()
    repo = ActivityRepository(session=session_mock)
    
    user_id = uuid4()
    
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    
    activity_list = [
        Activity(id=uuid4(), title="Atividade 1", user_id=user_id),
        Activity(id=uuid4(), title="Atividade 2", user_id=user_id)
    ]
    mock_scalars.all.return_value = activity_list
    mock_result.scalars.return_value = mock_scalars
    
    session_mock.execute.return_value = mock_result
    
    result = await repo.get_all_by_user(user_id)
    
    session_mock.execute.assert_awaited_once()
    assert result == activity_list

@pytest.mark.asyncio
async def test_update_activity():
    session_mock = AsyncMock()
    repo = ActivityRepository(session=session_mock)
    
    activity = Activity(id=uuid4(), title="Updated", user_id=uuid4())
    result = await repo.update(activity)
    
    assert result == activity

@pytest.mark.asyncio
async def test_soft_delete_activity():
    session_mock = AsyncMock()
    repo = ActivityRepository(session=session_mock)
    
    activity = Activity(id=uuid4(), title="Estudar", user_id=uuid4())
    assert activity.deleted_at is None
    
    result = await repo.soft_delete(activity)
    
    assert result.deleted_at is not None
    assert result == activity

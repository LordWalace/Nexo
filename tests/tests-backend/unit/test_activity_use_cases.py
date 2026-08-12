import uuid
from unittest.mock import AsyncMock

import pytest
from app.application.use_cases.activity import ActivityUseCases
from app.infrastructure.database.models.activity import Activity
from app.schemas.activity import ActivityCreate


@pytest.fixture
def mock_repo():
    return AsyncMock()


@pytest.fixture
def mock_session():
    return AsyncMock()


@pytest.fixture
def use_case(mock_repo, mock_session):
    return ActivityUseCases(mock_repo, mock_session)


@pytest.mark.asyncio
async def test_get_all_activities(use_case, mock_repo):
    mock_repo.get_all_by_user.return_value = [
        Activity(id=uuid.uuid4(), title="Read Book", user_id=uuid.uuid4())
    ]

    activities = await use_case.get_all_activities(user_id=uuid.uuid4())
    assert len(activities) == 1
    assert activities[0].title == "Read Book"
    mock_repo.get_all_by_user.assert_called_once()


@pytest.mark.asyncio
async def test_create_activity(use_case, mock_repo):
    user_id = uuid.uuid4()
    mock_repo.create.return_value = Activity(
        id=uuid.uuid4(), title="Code", user_id=user_id
    )

    activity_in = ActivityCreate(
        title="Code",
        description="Write Python",
        is_completed=False,
        category_id=uuid.uuid4(),
    )

    activity = await use_case.create_activity(user_id=user_id, activity_in=activity_in)
    assert activity.title == "Code"
    mock_repo.create.assert_called_once()

from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from app.application.use_cases.activity import ActivityUseCases
from app.core.exceptions import AppException
from app.infrastructure.database.models.activity import Activity
from app.schemas.activity import ActivityCreate, ActivityUpdate


@pytest.mark.asyncio
async def test_create_activity():
    mock_repo = AsyncMock()
    mock_session = AsyncMock()

    use_cases = ActivityUseCases(repository=mock_repo, session=mock_session)
    user_id = uuid4()
    cat_id = uuid4()
    act_in = ActivityCreate(title="Estudar", description="desc", category_id=cat_id)

    result = await use_cases.create_activity(user_id=user_id, activity_in=act_in)

    mock_repo.create.assert_awaited_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()
    assert result.title == "Estudar"
    assert result.description == "desc"
    assert result.category_id == cat_id
    assert result.user_id == user_id


@pytest.mark.asyncio
async def test_get_all_activities():
    mock_repo = AsyncMock()
    mock_session = AsyncMock()

    use_cases = ActivityUseCases(repository=mock_repo, session=mock_session)
    user_id = uuid4()

    expected_list = [
        Activity(id=uuid4(), title="Act1", user_id=user_id, category_id=uuid4())
    ]
    mock_repo.get_all_by_user.return_value = expected_list

    result = await use_cases.get_all_activities(user_id=user_id)

    mock_repo.get_all_by_user.assert_awaited_once_with(user_id)
    assert result == expected_list


@pytest.mark.asyncio
async def test_update_activity_success():
    mock_repo = AsyncMock()
    mock_session = AsyncMock()

    use_cases = ActivityUseCases(repository=mock_repo, session=mock_session)
    user_id = uuid4()
    act_id = uuid4()
    cat_id = uuid4()

    existing_act = Activity(
        id=act_id, title="Act1", description="desc", category_id=cat_id, user_id=user_id
    )
    mock_repo.get_by_id.return_value = existing_act

    new_cat_id = uuid4()
    update_data = ActivityUpdate(
        title="ActUpdated", description="newdesc", category_id=new_cat_id
    )

    result = await use_cases.update_activity(
        activity_id=act_id, user_id=user_id, activity_in=update_data
    )

    mock_repo.get_by_id.assert_awaited_once_with(act_id, user_id)
    mock_repo.update.assert_awaited_once_with(existing_act)
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()
    assert result.title == "ActUpdated"
    assert result.description == "newdesc"
    assert result.category_id == new_cat_id


@pytest.mark.asyncio
async def test_update_activity_not_found():
    mock_repo = AsyncMock()
    mock_session = AsyncMock()

    use_cases = ActivityUseCases(repository=mock_repo, session=mock_session)
    user_id = uuid4()
    act_id = uuid4()

    mock_repo.get_by_id.return_value = None
    update_data = ActivityUpdate(title="ActUpdated")

    with pytest.raises(AppException) as excinfo:
        await use_cases.update_activity(
            activity_id=act_id, user_id=user_id, activity_in=update_data
        )

    assert excinfo.value.code == "ACTIVITY_NOT_FOUND"


@pytest.mark.asyncio
async def test_delete_activity_success():
    mock_repo = AsyncMock()
    mock_session = AsyncMock()

    use_cases = ActivityUseCases(repository=mock_repo, session=mock_session)
    user_id = uuid4()
    act_id = uuid4()

    existing_act = Activity(
        id=act_id, title="Act1", category_id=uuid4(), user_id=user_id
    )
    mock_repo.get_by_id.return_value = existing_act

    await use_cases.delete_activity(activity_id=act_id, user_id=user_id)

    mock_repo.soft_delete.assert_awaited_once_with(existing_act)
    mock_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_activity_not_found():
    mock_repo = AsyncMock()
    mock_session = AsyncMock()

    use_cases = ActivityUseCases(repository=mock_repo, session=mock_session)
    user_id = uuid4()
    act_id = uuid4()

    mock_repo.get_by_id.return_value = None

    with pytest.raises(AppException) as excinfo:
        await use_cases.delete_activity(activity_id=act_id, user_id=user_id)

    assert excinfo.value.code == "ACTIVITY_NOT_FOUND"

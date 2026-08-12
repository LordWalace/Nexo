from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from app.infrastructure.database.models.category import Category
from app.infrastructure.database.repositories.category_repository import (
    CategoryRepository,
)


@pytest.mark.asyncio
async def test_create_category():
    session_mock = AsyncMock()
    repo = CategoryRepository(session=session_mock)

    category = Category(id=uuid4(), name="Estudos", user_id=uuid4())
    result = await repo.create(category)

    session_mock.add.assert_called_once_with(category)
    assert result == category


@pytest.mark.asyncio
async def test_get_by_id_category():
    session_mock = AsyncMock()
    repo = CategoryRepository(session=session_mock)

    cat_id = uuid4()
    user_id = uuid4()

    mock_result = MagicMock()
    mock_scalars = MagicMock()

    category = Category(id=cat_id, name="Estudos", user_id=user_id)
    mock_scalars.first.return_value = category
    mock_result.scalars.return_value = mock_scalars

    session_mock.execute.return_value = mock_result

    result = await repo.get_by_id(cat_id, user_id)

    session_mock.execute.assert_awaited_once()
    assert result == category


@pytest.mark.asyncio
async def test_get_all_by_user_category():
    session_mock = AsyncMock()
    repo = CategoryRepository(session=session_mock)

    user_id = uuid4()

    mock_result = MagicMock()
    mock_scalars = MagicMock()

    category_list = [
        Category(id=uuid4(), name="Estudos 1", user_id=user_id),
        Category(id=uuid4(), name="Estudos 2", user_id=user_id),
    ]
    mock_scalars.all.return_value = category_list
    mock_result.scalars.return_value = mock_scalars

    session_mock.execute.return_value = mock_result

    result = await repo.get_all_by_user(user_id)

    session_mock.execute.assert_awaited_once()
    assert result == category_list


@pytest.mark.asyncio
async def test_update_category():
    session_mock = AsyncMock()
    repo = CategoryRepository(session=session_mock)

    category = Category(id=uuid4(), name="Updated", user_id=uuid4())
    result = await repo.update(category)

    assert result == category
    # Session update is handled implicitly by SQLAlchemy tracking the object


@pytest.mark.asyncio
async def test_soft_delete_category():
    session_mock = AsyncMock()
    repo = CategoryRepository(session=session_mock)

    category = Category(id=uuid4(), name="Estudos", user_id=uuid4())
    assert category.deleted_at is None

    result = await repo.soft_delete(category)

    assert result.deleted_at is not None
    assert result == category

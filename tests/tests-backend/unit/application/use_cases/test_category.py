import pytest
from unittest.mock import AsyncMock
from uuid import uuid4
from datetime import datetime, UTC

from app.application.use_cases.category import CategoryUseCases
from app.infrastructure.database.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.core.exceptions import AppException

@pytest.mark.asyncio
async def test_create_category():
    mock_repo = AsyncMock()
    mock_session = AsyncMock()
    
    use_cases = CategoryUseCases(repository=mock_repo, session=mock_session)
    user_id = uuid4()
    cat_in = CategoryCreate(name="Estudos")
    
    result = await use_cases.create_category(user_id=user_id, category_in=cat_in)
    
    mock_repo.create.assert_awaited_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()
    assert result.name == "Estudos"
    assert result.user_id == user_id

@pytest.mark.asyncio
async def test_get_all_categories():
    mock_repo = AsyncMock()
    mock_session = AsyncMock()
    
    use_cases = CategoryUseCases(repository=mock_repo, session=mock_session)
    user_id = uuid4()
    
    expected_list = [Category(id=uuid4(), name="Cat1", user_id=user_id)]
    mock_repo.get_all_by_user.return_value = expected_list
    
    result = await use_cases.get_all_categories(user_id=user_id)
    
    mock_repo.get_all_by_user.assert_awaited_once_with(user_id)
    assert result == expected_list

@pytest.mark.asyncio
async def test_update_category_success():
    mock_repo = AsyncMock()
    mock_session = AsyncMock()
    
    use_cases = CategoryUseCases(repository=mock_repo, session=mock_session)
    user_id = uuid4()
    cat_id = uuid4()
    
    existing_cat = Category(id=cat_id, name="Cat1", user_id=user_id)
    mock_repo.get_by_id.return_value = existing_cat
    
    update_data = CategoryUpdate(name="CatUpdated")
    
    result = await use_cases.update_category(category_id=cat_id, user_id=user_id, category_in=update_data)
    
    mock_repo.get_by_id.assert_awaited_once_with(cat_id, user_id)
    mock_repo.update.assert_awaited_once_with(existing_cat)
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()
    assert result.name == "CatUpdated"

@pytest.mark.asyncio
async def test_update_category_not_found():
    mock_repo = AsyncMock()
    mock_session = AsyncMock()
    
    use_cases = CategoryUseCases(repository=mock_repo, session=mock_session)
    user_id = uuid4()
    cat_id = uuid4()
    
    mock_repo.get_by_id.return_value = None
    update_data = CategoryUpdate(name="CatUpdated")
    
    with pytest.raises(AppException) as excinfo:
        await use_cases.update_category(category_id=cat_id, user_id=user_id, category_in=update_data)
        
    assert excinfo.value.code == "CATEGORY_NOT_FOUND"

@pytest.mark.asyncio
async def test_delete_category_success():
    mock_repo = AsyncMock()
    mock_session = AsyncMock()
    
    use_cases = CategoryUseCases(repository=mock_repo, session=mock_session)
    user_id = uuid4()
    cat_id = uuid4()
    
    existing_cat = Category(id=cat_id, name="Cat1", user_id=user_id)
    mock_repo.get_by_id.return_value = existing_cat
    
    await use_cases.delete_category(category_id=cat_id, user_id=user_id)
    
    mock_repo.soft_delete.assert_awaited_once_with(existing_cat)
    mock_session.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_delete_category_not_found():
    mock_repo = AsyncMock()
    mock_session = AsyncMock()
    
    use_cases = CategoryUseCases(repository=mock_repo, session=mock_session)
    user_id = uuid4()
    cat_id = uuid4()
    
    mock_repo.get_by_id.return_value = None
    
    with pytest.raises(AppException) as excinfo:
        await use_cases.delete_category(category_id=cat_id, user_id=user_id)
        
    assert excinfo.value.code == "CATEGORY_NOT_FOUND"

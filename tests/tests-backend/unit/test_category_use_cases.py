import pytest
import uuid
from unittest.mock import AsyncMock

from app.application.use_cases.category import CategoryUseCases
from app.infrastructure.database.models.category import Category
from app.schemas.category import CategoryCreate

@pytest.fixture
def mock_repo():
    return AsyncMock()

@pytest.fixture
def mock_session():
    return AsyncMock()

@pytest.fixture
def use_case(mock_repo, mock_session):
    return CategoryUseCases(mock_repo, mock_session)

@pytest.mark.asyncio
async def test_get_all_categories(use_case, mock_repo):
    mock_repo.get_all_by_user.return_value = [
        Category(id=uuid.uuid4(), name="Work", user_id=uuid.uuid4())
    ]
    
    categories = await use_case.get_all_categories(user_id=uuid.uuid4())
    assert len(categories) == 1
    assert categories[0].name == "Work"
    mock_repo.get_all_by_user.assert_called_once()

@pytest.mark.asyncio
async def test_create_category(use_case, mock_repo):
    user_id = uuid.uuid4()
    mock_repo.create.return_value = Category(id=uuid.uuid4(), name="Study", user_id=user_id)
    
    category_in = CategoryCreate(name="Study", color="#000000")
    
    category = await use_case.create_category(user_id=user_id, category_in=category_in)
    assert category.name == "Study"
    mock_repo.create.assert_called_once()

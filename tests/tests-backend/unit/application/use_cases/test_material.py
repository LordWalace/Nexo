import pytest
from unittest.mock import AsyncMock
from uuid import uuid4

from app.application.use_cases.material import MaterialUseCases
from app.infrastructure.database.models.material import Material
from app.schemas.material import MaterialCreate, MaterialUpdate
from app.core.exceptions import AppException

@pytest.mark.asyncio
async def test_create_material():
    mock_repo = AsyncMock()
    mock_session = AsyncMock()
    
    use_cases = MaterialUseCases(repository=mock_repo, session=mock_session)
    user_id = uuid4()
    mat_in = MaterialCreate(name="Livro", url="http://test")
    
    result = await use_cases.create_material(user_id=user_id, material_in=mat_in)
    
    mock_repo.create.assert_awaited_once()
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()
    assert result.name == "Livro"
    assert result.url == "http://test"
    assert result.user_id == user_id

@pytest.mark.asyncio
async def test_get_all_materials():
    mock_repo = AsyncMock()
    mock_session = AsyncMock()
    
    use_cases = MaterialUseCases(repository=mock_repo, session=mock_session)
    user_id = uuid4()
    
    expected_list = [Material(id=uuid4(), name="Mat1", url="http://test", user_id=user_id)]
    mock_repo.get_all_by_user.return_value = expected_list
    
    result = await use_cases.get_all_materials(user_id=user_id)
    
    mock_repo.get_all_by_user.assert_awaited_once_with(user_id)
    assert result == expected_list

@pytest.mark.asyncio
async def test_update_material_success():
    mock_repo = AsyncMock()
    mock_session = AsyncMock()
    
    use_cases = MaterialUseCases(repository=mock_repo, session=mock_session)
    user_id = uuid4()
    mat_id = uuid4()
    
    existing_mat = Material(id=mat_id, name="Mat1", url="url", user_id=user_id)
    mock_repo.get_by_id.return_value = existing_mat
    
    update_data = MaterialUpdate(name="MatUpdated", url="newurl")
    
    result = await use_cases.update_material(material_id=mat_id, user_id=user_id, material_in=update_data)
    
    mock_repo.get_by_id.assert_awaited_once_with(mat_id, user_id)
    mock_repo.update.assert_awaited_once_with(existing_mat)
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once()
    assert result.name == "MatUpdated"
    assert result.url == "newurl"

@pytest.mark.asyncio
async def test_update_material_not_found():
    mock_repo = AsyncMock()
    mock_session = AsyncMock()
    
    use_cases = MaterialUseCases(repository=mock_repo, session=mock_session)
    user_id = uuid4()
    mat_id = uuid4()
    
    mock_repo.get_by_id.return_value = None
    update_data = MaterialUpdate(name="MatUpdated")
    
    with pytest.raises(AppException) as excinfo:
        await use_cases.update_material(material_id=mat_id, user_id=user_id, material_in=update_data)
        
    assert excinfo.value.code == "MATERIAL_NOT_FOUND"

@pytest.mark.asyncio
async def test_delete_material_success():
    mock_repo = AsyncMock()
    mock_session = AsyncMock()
    
    use_cases = MaterialUseCases(repository=mock_repo, session=mock_session)
    user_id = uuid4()
    mat_id = uuid4()
    
    existing_mat = Material(id=mat_id, name="Mat1", user_id=user_id)
    mock_repo.get_by_id.return_value = existing_mat
    
    await use_cases.delete_material(material_id=mat_id, user_id=user_id)
    
    mock_repo.soft_delete.assert_awaited_once_with(existing_mat)
    mock_session.commit.assert_awaited_once()

@pytest.mark.asyncio
async def test_delete_material_not_found():
    mock_repo = AsyncMock()
    mock_session = AsyncMock()
    
    use_cases = MaterialUseCases(repository=mock_repo, session=mock_session)
    user_id = uuid4()
    mat_id = uuid4()
    
    mock_repo.get_by_id.return_value = None
    
    with pytest.raises(AppException) as excinfo:
        await use_cases.delete_material(material_id=mat_id, user_id=user_id)
        
    assert excinfo.value.code == "MATERIAL_NOT_FOUND"

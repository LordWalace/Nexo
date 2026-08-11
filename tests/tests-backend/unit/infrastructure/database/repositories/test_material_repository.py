import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
from datetime import datetime, UTC

from app.infrastructure.database.models.material import Material
from app.infrastructure.database.repositories.material_repository import MaterialRepository

@pytest.mark.asyncio
async def test_create_material():
    session_mock = AsyncMock()
    repo = MaterialRepository(session=session_mock)
    
    material = Material(id=uuid4(), name="Livro", user_id=uuid4(), url="test")
    result = await repo.create(material)
    
    session_mock.add.assert_called_once_with(material)
    assert result == material

@pytest.mark.asyncio
async def test_get_by_id_material():
    session_mock = AsyncMock()
    repo = MaterialRepository(session=session_mock)
    
    mat_id = uuid4()
    user_id = uuid4()
    
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    
    material = Material(id=mat_id, name="Livro", user_id=user_id, url="test")
    mock_scalars.first.return_value = material
    mock_result.scalars.return_value = mock_scalars
    
    session_mock.execute.return_value = mock_result
    
    result = await repo.get_by_id(mat_id, user_id)
    
    session_mock.execute.assert_awaited_once()
    assert result == material

@pytest.mark.asyncio
async def test_get_all_by_user_material():
    session_mock = AsyncMock()
    repo = MaterialRepository(session=session_mock)
    
    user_id = uuid4()
    
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    
    material_list = [
        Material(id=uuid4(), name="Mat 1", user_id=user_id, url="test"),
        Material(id=uuid4(), name="Mat 2", user_id=user_id, url="test")
    ]
    mock_scalars.all.return_value = material_list
    mock_result.scalars.return_value = mock_scalars
    
    session_mock.execute.return_value = mock_result
    
    result = await repo.get_all_by_user(user_id)
    
    session_mock.execute.assert_awaited_once()
    assert result == material_list

@pytest.mark.asyncio
async def test_update_material():
    session_mock = AsyncMock()
    repo = MaterialRepository(session=session_mock)
    
    material = Material(id=uuid4(), name="Updated", user_id=uuid4(), url="test")
    result = await repo.update(material)
    
    assert result == material

@pytest.mark.asyncio
async def test_soft_delete_material():
    session_mock = AsyncMock()
    repo = MaterialRepository(session=session_mock)
    
    material = Material(id=uuid4(), name="Livro", user_id=uuid4(), url="test")
    assert material.deleted_at is None
    
    result = await repo.soft_delete(material)
    
    assert result.deleted_at is not None
    assert result == material

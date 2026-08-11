from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.material import MaterialUseCases
from app.core.dependencies import get_current_user, get_db
from app.infrastructure.database.models.user import User
from app.infrastructure.database.repositories.material_repository import (
    MaterialRepository,
)
from app.schemas.material import MaterialCreate, MaterialResponse, MaterialUpdate

router = APIRouter(prefix="/materials", tags=["materials"])


@router.post("/", response_model=MaterialResponse, status_code=status.HTTP_201_CREATED)
async def create_material(
    material_in: MaterialCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> "Any":
    repository = MaterialRepository(session)
    use_cases = MaterialUseCases(repository, session)
    return await use_cases.create_material(current_user.id, material_in)


@router.get("/", response_model=list[MaterialResponse])
async def get_materials(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> "Any":
    repository = MaterialRepository(session)
    use_cases = MaterialUseCases(repository, session)
    return await use_cases.get_all_materials(current_user.id)


@router.patch("/{material_id}", response_model=MaterialResponse)
async def update_material(
    material_id: UUID,
    material_in: MaterialUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> "Any":
    repository = MaterialRepository(session)
    use_cases = MaterialUseCases(repository, session)
    return await use_cases.update_material(material_id, current_user.id, material_in)


@router.delete("/{material_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_material(
    material_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> None:
    repository = MaterialRepository(session)
    use_cases = MaterialUseCases(repository, session)
    await use_cases.delete_material(material_id, current_user.id)

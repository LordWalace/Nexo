from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.category import CategoryUseCases
from app.core.dependencies import get_current_user, get_db
from app.infrastructure.database.models.user import User
from app.infrastructure.database.repositories.category_repository import (
    CategoryRepository,
)
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_in: CategoryCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> "Any":
    repository = CategoryRepository(session)
    use_cases = CategoryUseCases(repository, session)
    return await use_cases.create_category(current_user.id, category_in)


@router.get("/", response_model=list[CategoryResponse])
async def get_categories(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> "Any":
    repository = CategoryRepository(session)
    use_cases = CategoryUseCases(repository, session)
    return await use_cases.get_all_categories(current_user.id)


@router.patch("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: UUID,
    category_in: CategoryUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> "Any":
    repository = CategoryRepository(session)
    use_cases = CategoryUseCases(repository, session)
    return await use_cases.update_category(category_id, current_user.id, category_in)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> None:
    repository = CategoryRepository(session)
    use_cases = CategoryUseCases(repository, session)
    await use_cases.delete_category(category_id, current_user.id)

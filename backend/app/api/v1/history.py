from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.history import HistoryUseCases
from app.core.dependencies import get_current_user, get_db
from app.infrastructure.database.models.user import User
from app.infrastructure.database.repositories.history_repository import (
    HistoryRepository,
)
from app.schemas.history import HistoryCreate, HistoryResponse, HistoryUpdate

router = APIRouter(prefix="/history", tags=["history"])


@router.post("/", response_model=HistoryResponse, status_code=status.HTTP_201_CREATED)
async def create_history(
    history_in: HistoryCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> "Any":
    repository = HistoryRepository(session)
    use_cases = HistoryUseCases(repository, session)
    return await use_cases.create_history(current_user.id, history_in)


@router.get("/", response_model=list[HistoryResponse])
async def get_history(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> "Any":
    repository = HistoryRepository(session)
    use_cases = HistoryUseCases(repository, session)
    return await use_cases.get_all_history(current_user.id)


@router.patch("/{period_id}", response_model=HistoryResponse)
async def update_history(
    period_id: UUID,
    history_in: HistoryUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> "Any":
    repository = HistoryRepository(session)
    use_cases = HistoryUseCases(repository, session)
    return await use_cases.update_history(period_id, current_user.id, history_in)


@router.delete("/{period_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_history(
    period_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> None:
    repository = HistoryRepository(session)
    use_cases = HistoryUseCases(repository, session)
    await use_cases.delete_history(period_id, current_user.id)

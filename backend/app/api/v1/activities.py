from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.activity import ActivityUseCases
from app.core.dependencies import get_current_user, get_db
from app.infrastructure.database.models.user import User
from app.infrastructure.database.repositories.activity_repository import (
    ActivityRepository,
)
from app.schemas.activity import ActivityCreate, ActivityResponse, ActivityUpdate

router = APIRouter(prefix="/activities", tags=["activities"])


@router.post("/", response_model=ActivityResponse, status_code=status.HTTP_201_CREATED)
async def create_activity(
    activity_in: ActivityCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> "Any":
    repository = ActivityRepository(session)
    use_cases = ActivityUseCases(repository, session)
    return await use_cases.create_activity(current_user.id, activity_in)


@router.get("/", response_model=list[ActivityResponse])
async def get_activities(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> "Any":
    repository = ActivityRepository(session)
    use_cases = ActivityUseCases(repository, session)
    return await use_cases.get_all_activities(current_user.id)


@router.patch("/{activity_id}", response_model=ActivityResponse)
async def update_activity(
    activity_id: UUID,
    activity_in: ActivityUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> "Any":
    repository = ActivityRepository(session)
    use_cases = ActivityUseCases(repository, session)
    return await use_cases.update_activity(activity_id, current_user.id, activity_in)


@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_activity(
    activity_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> None:
    repository = ActivityRepository(session)
    use_cases = ActivityUseCases(repository, session)
    await use_cases.delete_activity(activity_id, current_user.id)

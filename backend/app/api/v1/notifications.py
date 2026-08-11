from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.notification import NotificationUseCases
from app.core.dependencies import get_current_user, get_db
from app.infrastructure.database.models.user import User
from app.infrastructure.database.repositories.notification_repository import (
    NotificationRepository,
)
from app.schemas.notification import NotificationCreate, NotificationResponse

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("/", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
async def create_notification(
    notification_in: NotificationCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> "Any":
    repository = NotificationRepository(session)
    use_cases = NotificationUseCases(repository, session)
    return await use_cases.create_notification(current_user.id, notification_in)


@router.get("/", response_model=list[NotificationResponse])
async def get_notifications(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> "Any":
    repository = NotificationRepository(session)
    use_cases = NotificationUseCases(repository, session)
    return await use_cases.get_all_notifications(current_user.id)


@router.patch("/{notification_id}/read", response_model=NotificationResponse)
async def mark_notification_as_read(
    notification_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> "Any":
    repository = NotificationRepository(session)
    use_cases = NotificationUseCases(repository, session)
    return await use_cases.mark_as_read(notification_id, current_user.id)

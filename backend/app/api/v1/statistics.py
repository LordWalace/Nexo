from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.statistics import StatisticsUseCases
from app.core.dependencies import get_current_user, get_db
from app.infrastructure.database.models.user import User
from app.infrastructure.database.repositories.activity_repository import (
    ActivityRepository,
)
from app.infrastructure.database.repositories.history_repository import (
    HistoryRepository,
)
from app.schemas.statistics import StatisticsResponse

router = APIRouter(prefix="/statistics", tags=["statistics"])


@router.get("/", response_model=StatisticsResponse)
async def get_statistics(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> "Any":
    activity_repo = ActivityRepository(session)
    history_repo = HistoryRepository(session)
    use_cases = StatisticsUseCases(activity_repo, history_repo, session)
    return await use_cases.get_user_statistics(current_user.id)

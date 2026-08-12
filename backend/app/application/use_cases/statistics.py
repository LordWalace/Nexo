from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.activity_repository import IActivityRepository
from app.domain.repositories.history_repository import IHistoryRepository
from app.schemas.statistics import StatisticsResponse


class StatisticsUseCases:
    def __init__(
        self,
        activity_repo: IActivityRepository,
        history_repo: IHistoryRepository,
        session: AsyncSession,
    ):
        self.activity_repo = activity_repo
        self.history_repo = history_repo
        self.session = session

    async def get_user_statistics(self, user_id: UUID) -> StatisticsResponse:
        activities = await self.activity_repo.get_all_by_user(user_id)
        history = await self.history_repo.get_all_by_user(user_id)

        total_activities = len(activities)
        total_execution_periods = len(history)

        return StatisticsResponse(
            total_activities=total_activities,
            total_execution_periods=total_execution_periods,
        )

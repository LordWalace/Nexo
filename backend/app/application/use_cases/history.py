from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AppException
from app.domain.repositories.history_repository import IHistoryRepository
from app.infrastructure.database.models.execution_period import ActivityExecutionPeriod
from app.schemas.history import HistoryCreate, HistoryUpdate


class HistoryUseCases:
    def __init__(self, repository: IHistoryRepository, session: AsyncSession):
        self.repository = repository
        self.session = session

    async def create_history(
        self, user_id: UUID, history_in: HistoryCreate
    ) -> ActivityExecutionPeriod:
        period = ActivityExecutionPeriod(
            activity_id=history_in.activity_id,
            user_id=user_id,
            start_time=history_in.start_time,
            end_time=history_in.end_time,
        )
        await self.repository.create(period)
        await self.session.commit()
        await self.session.refresh(period)
        return period

    async def get_all_history(self, user_id: UUID) -> list[ActivityExecutionPeriod]:
        return await self.repository.get_all_by_user(user_id)

    async def update_history(
        self, period_id: UUID, user_id: UUID, history_in: HistoryUpdate
    ) -> ActivityExecutionPeriod:
        period = await self.repository.get_by_id(period_id, user_id)
        if not period:
            raise AppException(
                code="HISTORY_NOT_FOUND",
                message="Período de execução não encontrado.",
                status_code=404,
            )

        if history_in.start_time is not None:
            period.start_time = history_in.start_time
        if history_in.end_time is not None:
            period.end_time = history_in.end_time

        await self.repository.update(period)
        await self.session.commit()
        await self.session.refresh(period)
        return period

    async def delete_history(self, period_id: UUID, user_id: UUID) -> None:
        period = await self.repository.get_by_id(period_id, user_id)
        if not period:
            raise AppException(
                code="HISTORY_NOT_FOUND",
                message="Período de execução não encontrado.",
                status_code=404,
            )

        await self.repository.delete(period)
        await self.session.commit()

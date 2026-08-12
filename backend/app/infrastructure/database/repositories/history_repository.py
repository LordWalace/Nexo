from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.history_repository import IHistoryRepository
from app.infrastructure.database.models.execution_period import ActivityExecutionPeriod


class HistoryRepository(IHistoryRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, period: ActivityExecutionPeriod) -> ActivityExecutionPeriod:
        self.session.add(period)
        return period

    async def get_by_id(
        self, period_id: UUID, user_id: UUID
    ) -> ActivityExecutionPeriod | None:
        stmt = select(ActivityExecutionPeriod).where(
            ActivityExecutionPeriod.id == period_id,
            ActivityExecutionPeriod.user_id == user_id,
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all_by_user(self, user_id: UUID) -> list[ActivityExecutionPeriod]:
        stmt = (
            select(ActivityExecutionPeriod)
            .where(ActivityExecutionPeriod.user_id == user_id)
            .order_by(ActivityExecutionPeriod.start_time.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update(self, period: ActivityExecutionPeriod) -> ActivityExecutionPeriod:
        return period

    async def delete(self, period: ActivityExecutionPeriod) -> None:
        await self.session.delete(period)

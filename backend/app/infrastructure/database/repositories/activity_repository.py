from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.activity_repository import IActivityRepository
from app.infrastructure.database.models.activity import Activity


class ActivityRepository(IActivityRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, activity: Activity) -> Activity:
        self.session.add(activity)
        return activity

    async def get_by_id(self, activity_id: UUID, user_id: UUID) -> Activity | None:
        stmt = select(Activity).where(
            Activity.id == activity_id,
            Activity.user_id == user_id,
            Activity.deleted_at.is_(None),
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all_by_user(self, user_id: UUID) -> list[Activity]:
        stmt = (
            select(Activity)
            .where(Activity.user_id == user_id, Activity.deleted_at.is_(None))
            .order_by(Activity.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update(self, activity: Activity) -> Activity:
        return activity

    async def soft_delete(self, activity: Activity) -> Activity:
        activity.deleted_at = datetime.now(UTC)
        return activity

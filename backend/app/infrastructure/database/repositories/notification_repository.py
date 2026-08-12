from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.notification_repository import INotificationRepository
from app.infrastructure.database.models.notification import Notification


class NotificationRepository(INotificationRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, notification: Notification) -> Notification:
        self.session.add(notification)
        return notification

    async def get_by_id(
        self, notification_id: UUID, user_id: UUID
    ) -> Notification | None:
        stmt = select(Notification).where(
            Notification.id == notification_id, Notification.user_id == user_id
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all_by_user(self, user_id: UUID) -> list[Notification]:
        stmt = (
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update(self, notification: Notification) -> Notification:
        return notification

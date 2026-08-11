from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AppException
from app.domain.repositories.notification_repository import INotificationRepository
from app.infrastructure.database.models.notification import Notification
from app.schemas.notification import NotificationCreate


class NotificationUseCases:
    def __init__(self, repository: INotificationRepository, session: AsyncSession):
        self.repository = repository
        self.session = session

    async def create_notification(
        self, user_id: UUID, notification_in: NotificationCreate
    ) -> Notification:
        notification = Notification(
            user_id=user_id,
            title=notification_in.title,
            message=notification_in.message,
        )
        await self.repository.create(notification)
        await self.session.commit()
        await self.session.refresh(notification)
        return notification

    async def get_all_notifications(self, user_id: UUID) -> list[Notification]:
        return await self.repository.get_all_by_user(user_id)

    async def mark_as_read(self, notification_id: UUID, user_id: UUID) -> Notification:
        notification = await self.repository.get_by_id(notification_id, user_id)
        if not notification:
            raise AppException(
                code="NOTIFICATION_NOT_FOUND",
                message="Notificação não encontrada.",
                status_code=404,
            )

        notification.is_read = True

        await self.repository.update(notification)
        await self.session.commit()
        await self.session.refresh(notification)
        return notification

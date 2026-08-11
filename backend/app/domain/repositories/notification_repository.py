from abc import ABC, abstractmethod
from uuid import UUID

from app.infrastructure.database.models.notification import Notification


class INotificationRepository(ABC):
    @abstractmethod
    async def create(self, notification: Notification) -> Notification:
        pass

    @abstractmethod
    async def get_by_id(self, notification_id: UUID, user_id: UUID) -> Notification | None:
        pass

    @abstractmethod
    async def get_all_by_user(self, user_id: UUID) -> list[Notification]:
        pass

    @abstractmethod
    async def update(self, notification: Notification) -> Notification:
        pass

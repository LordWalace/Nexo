from abc import ABC, abstractmethod
from uuid import UUID

from app.infrastructure.database.models.activity import Activity


class IActivityRepository(ABC):
    @abstractmethod
    async def create(self, activity: Activity) -> Activity:
        pass

    @abstractmethod
    async def get_by_id(self, activity_id: UUID, user_id: UUID) -> Activity | None:
        pass

    @abstractmethod
    async def get_all_by_user(self, user_id: UUID) -> list[Activity]:
        pass

    @abstractmethod
    async def update(self, activity: Activity) -> Activity:
        pass

    @abstractmethod
    async def soft_delete(self, activity: Activity) -> Activity:
        pass

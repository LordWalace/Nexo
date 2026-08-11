from abc import ABC, abstractmethod
from uuid import UUID

from app.infrastructure.database.models.execution_period import ActivityExecutionPeriod


class IHistoryRepository(ABC):
    @abstractmethod
    async def create(self, period: ActivityExecutionPeriod) -> ActivityExecutionPeriod:
        pass

    @abstractmethod
    async def get_by_id(
        self, period_id: UUID, user_id: UUID
    ) -> ActivityExecutionPeriod | None:
        pass

    @abstractmethod
    async def get_all_by_user(self, user_id: UUID) -> list[ActivityExecutionPeriod]:
        pass

    @abstractmethod
    async def update(self, period: ActivityExecutionPeriod) -> ActivityExecutionPeriod:
        pass

    @abstractmethod
    async def delete(self, period: ActivityExecutionPeriod) -> None:
        pass

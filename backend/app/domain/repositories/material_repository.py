from abc import ABC, abstractmethod
from uuid import UUID

from app.infrastructure.database.models.material import Material


class IMaterialRepository(ABC):
    @abstractmethod
    async def create(self, material: Material) -> Material:
        pass

    @abstractmethod
    async def get_by_id(self, material_id: UUID, user_id: UUID) -> Material | None:
        pass

    @abstractmethod
    async def get_all_by_user(self, user_id: UUID) -> list[Material]:
        pass

    @abstractmethod
    async def update(self, material: Material) -> Material:
        pass

    @abstractmethod
    async def soft_delete(self, material: Material) -> Material:
        pass

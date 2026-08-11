from abc import ABC, abstractmethod
from uuid import UUID

from app.infrastructure.database.models.category import Category


class ICategoryRepository(ABC):
    @abstractmethod
    async def create(self, category: Category) -> Category:
        pass

    @abstractmethod
    async def get_by_id(self, category_id: UUID, user_id: UUID) -> Category | None:
        pass

    @abstractmethod
    async def get_all_by_user(self, user_id: UUID) -> list[Category]:
        pass

    @abstractmethod
    async def update(self, category: Category) -> Category:
        pass

    @abstractmethod
    async def soft_delete(self, category: Category) -> Category:
        pass

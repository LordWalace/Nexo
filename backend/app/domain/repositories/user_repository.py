from abc import ABC, abstractmethod
from uuid import UUID

from app.infrastructure.database.models.user import User


class IUserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: UUID) -> User | None:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    async def get_active_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        pass

    @abstractmethod
    async def soft_delete(self, user: User) -> User:
        pass

    @abstractmethod
    async def restore(self, user: User) -> User:
        pass

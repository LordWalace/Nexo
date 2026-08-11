from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.domain.exceptions.user import DuplicateEmailException, UserNotFoundException
from app.infrastructure.database.models.user import User
from app.infrastructure.database.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserUseCases:
    def __init__(self, repository: UserRepository, session: AsyncSession):
        self.repository = repository
        self.session = session

    async def create_user(self, user_in: UserCreate) -> User:
        if await self.repository.exists_by_email(user_in.email):
            raise DuplicateEmailException()

        user = User(
            name=user_in.name,
            email=user_in.email,
            password_hash=get_password_hash(user_in.password),
        )
        await self.repository.create(user)
        try:
            await self.session.commit()
            await self.session.refresh(user)
        except IntegrityError:
            await self.session.rollback()
            raise DuplicateEmailException()

        return user

    async def get_user(self, user_id: UUID) -> User:
        user = await self.repository.get_by_id(user_id)
        if not user or user.is_deleted:
            raise UserNotFoundException()
        return user

    async def update_user(self, user_id: UUID, user_in: UserUpdate) -> User:
        user = await self.get_user(user_id)
        if user_in.name is not None:
            user.name = user_in.name
        if user_in.is_active is not None:
            user.is_active = user_in.is_active

        await self.repository.update(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def soft_delete_user(self, user_id: UUID) -> User:
        user = await self.get_user(user_id)
        await self.repository.soft_delete(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def restore_user(self, user_id: UUID) -> User:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundException()
        await self.repository.restore(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

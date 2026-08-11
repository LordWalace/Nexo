from collections.abc import AsyncGenerator
from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AppException
from app.core.security import decode_access_token
from app.infrastructure.database.models.user import User
from app.infrastructure.database.repositories.user_repository import UserRepository
from app.infrastructure.database.session import AsyncSessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_current_user(
    token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db)
) -> User:
    subject = decode_access_token(token)
    try:
        user_id = UUID(subject)
    except ValueError:
        raise AppException(
            code="TOKEN_INVALID_SUBJECT",
            message="O token possui um subject inválido.",
            status_code=401,
        )

    repository = UserRepository(session)
    user = await repository.get_by_id(user_id)
    if not user or user.is_deleted or not user.is_active:
        raise AppException(
            code="USER_NOT_FOUND_OR_INACTIVE",
            message="Usuário não encontrado ou inativo.",
            status_code=401,
        )

    return user

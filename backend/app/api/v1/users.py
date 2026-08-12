from typing import Any

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.user import UserUseCases
from app.core.dependencies import get_current_user, get_db
from app.infrastructure.database.models.user import User
from app.infrastructure.database.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate, session: AsyncSession = Depends(get_db)
) -> "Any":
    repository = UserRepository(session)
    use_cases = UserUseCases(repository, session)
    return await use_cases.create_user(user_in)


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)) -> "Any":
    return current_user

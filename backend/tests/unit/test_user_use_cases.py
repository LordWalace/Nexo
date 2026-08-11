from datetime import UTC, datetime
from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError

from app.application.use_cases.user import UserUseCases
from app.core.exceptions import AppException
from app.core.security import create_access_token, decode_access_token
from app.domain.exceptions.user import DuplicateEmailException, UserNotFoundException
from app.infrastructure.database.models.user import User
from app.schemas.user import UserCreate


class MockUserRepository:
    def __init__(self):
        self.users = {}

    async def create(self, user: User) -> User:
        self.users[user.email] = user
        return user

    async def get_by_id(self, user_id: UUID) -> User | None:
        for u in self.users.values():
            if u.id == user_id:
                return u
        return None

    async def get_by_email(self, email: str) -> User | None:
        return self.users.get(email)

    async def get_active_by_email(self, email: str) -> User | None:
        u = self.users.get(email)
        if u and not u.is_deleted:
            return u
        return None

    async def exists_by_email(self, email: str) -> bool:
        return await self.get_active_by_email(email) is not None

    async def update(self, user: User) -> User:
        return user

    async def soft_delete(self, user: User) -> User:
        user.deleted_at = datetime.now(UTC)
        return user

    async def restore(self, user: User) -> User:
        user.deleted_at = None
        return user


class MockSession:
    async def commit(self):
        pass

    async def rollback(self):
        pass

    async def refresh(self, instance):
        if not instance.id:
            instance.id = uuid4()


@pytest.fixture
def mock_repo():
    return MockUserRepository()


@pytest.fixture
def mock_session():
    return MockSession()


@pytest.mark.asyncio
async def test_create_user(mock_repo, mock_session):
    use_cases = UserUseCases(repository=mock_repo, session=mock_session)
    user_in = UserCreate(name="Test", email="test@example.com", password="password123")
    user = await use_cases.create_user(user_in)

    assert user.name == "Test"
    assert user.email == "test@example.com"
    assert user.id is not None
    assert await mock_repo.exists_by_email("test@example.com") is True


@pytest.mark.asyncio
async def test_create_user_duplicate_email(mock_repo, mock_session):
    use_cases = UserUseCases(repository=mock_repo, session=mock_session)
    user_in = UserCreate(name="Test", email="test@example.com", password="password123")
    await use_cases.create_user(user_in)

    with pytest.raises(DuplicateEmailException):
        await use_cases.create_user(user_in)


@pytest.mark.asyncio
async def test_soft_delete_and_restore(mock_repo, mock_session):
    use_cases = UserUseCases(repository=mock_repo, session=mock_session)
    user_in = UserCreate(name="Test", email="test@example.com", password="password123")
    user = await use_cases.create_user(user_in)

    deleted_user = await use_cases.soft_delete_user(user.id)
    assert deleted_user.is_deleted is True

    with pytest.raises(UserNotFoundException):
        await use_cases.get_user(user.id)

    restored_user = await use_cases.restore_user(user.id)
    assert restored_user.is_deleted is False


def test_user_schema_validation():
    # Validação de email (falha)
    with pytest.raises(ValidationError):
        UserCreate(name="Test", email="not-an-email", password="123")

    # Validação de nome (falha)
    with pytest.raises(ValidationError):
        UserCreate(name="   ", email="test@example.com", password="password123")


def test_decode_access_token_expired(mock_env_vars):
    from datetime import timedelta

    token = create_access_token(subject="user1", expires_delta=timedelta(seconds=-1))
    with pytest.raises(AppException) as exc:
        decode_access_token(token)
    assert exc.value.code == "TOKEN_EXPIRED"


def test_decode_access_token_invalid_signature(mock_env_vars):
    token = create_access_token(subject="user1")
    invalid_token = token[:-5] + "aaaaa"
    with pytest.raises(AppException) as exc:
        decode_access_token(invalid_token)
    assert exc.value.code == "TOKEN_INVALID_SIGNATURE"

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.category_repository import ICategoryRepository
from app.infrastructure.database.models.category import Category


class CategoryRepository(ICategoryRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, category: Category) -> Category:
        self.session.add(category)
        return category

    async def get_by_id(self, category_id: UUID, user_id: UUID) -> Category | None:
        stmt = select(Category).where(
            Category.id == category_id,
            Category.user_id == user_id,
            Category.deleted_at.is_(None),
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all_by_user(self, user_id: UUID) -> list[Category]:
        stmt = (
            select(Category)
            .where(Category.user_id == user_id, Category.deleted_at.is_(None))
            .order_by(Category.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update(self, category: Category) -> Category:
        return category

    async def soft_delete(self, category: Category) -> Category:
        category.deleted_at = datetime.now(UTC)
        return category

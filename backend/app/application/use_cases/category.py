from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AppException
from app.domain.repositories.category_repository import ICategoryRepository
from app.infrastructure.database.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryUseCases:
    def __init__(self, repository: ICategoryRepository, session: AsyncSession):
        self.repository = repository
        self.session = session

    async def create_category(
        self, user_id: UUID, category_in: CategoryCreate
    ) -> Category:
        category = Category(name=category_in.name, user_id=user_id)
        await self.repository.create(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def get_all_categories(self, user_id: UUID) -> list[Category]:
        return await self.repository.get_all_by_user(user_id)

    async def update_category(
        self, category_id: UUID, user_id: UUID, category_in: CategoryUpdate
    ) -> Category:
        category = await self.repository.get_by_id(category_id, user_id)
        if not category:
            raise AppException(
                code="CATEGORY_NOT_FOUND",
                message="Categoria não encontrada.",
                status_code=404,
            )

        if category_in.name is not None:
            category.name = category_in.name

        await self.repository.update(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def delete_category(self, category_id: UUID, user_id: UUID) -> None:
        category = await self.repository.get_by_id(category_id, user_id)
        if not category:
            raise AppException(
                code="CATEGORY_NOT_FOUND",
                message="Categoria não encontrada.",
                status_code=404,
            )

        await self.repository.soft_delete(category)
        await self.session.commit()

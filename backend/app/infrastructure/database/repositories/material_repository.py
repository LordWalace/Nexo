from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.material_repository import IMaterialRepository
from app.infrastructure.database.models.material import Material


class MaterialRepository(IMaterialRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, material: Material) -> Material:
        self.session.add(material)
        return material

    async def get_by_id(self, material_id: UUID, user_id: UUID) -> Material | None:
        stmt = select(Material).where(
            Material.id == material_id,
            Material.user_id == user_id,
            Material.deleted_at.is_(None)
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_all_by_user(self, user_id: UUID) -> list[Material]:
        stmt = select(Material).where(
            Material.user_id == user_id,
            Material.deleted_at.is_(None)
        ).order_by(Material.created_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update(self, material: Material) -> Material:
        return material

    async def soft_delete(self, material: Material) -> Material:
        material.deleted_at = datetime.now(UTC)
        return material

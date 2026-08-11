from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AppException
from app.domain.repositories.material_repository import IMaterialRepository
from app.infrastructure.database.models.material import Material
from app.schemas.material import MaterialCreate, MaterialUpdate


class MaterialUseCases:
    def __init__(self, repository: IMaterialRepository, session: AsyncSession):
        self.repository = repository
        self.session = session

    async def create_material(
        self, user_id: UUID, material_in: MaterialCreate
    ) -> Material:
        material = Material(name=material_in.name, url=material_in.url, user_id=user_id)
        await self.repository.create(material)
        await self.session.commit()
        await self.session.refresh(material)
        return material

    async def get_all_materials(self, user_id: UUID) -> list[Material]:
        return await self.repository.get_all_by_user(user_id)

    async def update_material(
        self, material_id: UUID, user_id: UUID, material_in: MaterialUpdate
    ) -> Material:
        material = await self.repository.get_by_id(material_id, user_id)
        if not material:
            raise AppException(
                code="MATERIAL_NOT_FOUND",
                message="Material não encontrado.",
                status_code=404,
            )

        if material_in.name is not None:
            material.name = material_in.name
        if material_in.url is not None:
            material.url = material_in.url

        await self.repository.update(material)
        await self.session.commit()
        await self.session.refresh(material)
        return material

    async def delete_material(self, material_id: UUID, user_id: UUID) -> None:
        material = await self.repository.get_by_id(material_id, user_id)
        if not material:
            raise AppException(
                code="MATERIAL_NOT_FOUND",
                message="Material não encontrado.",
                status_code=404,
            )

        await self.repository.soft_delete(material)
        await self.session.commit()

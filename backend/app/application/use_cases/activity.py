from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AppException
from app.domain.repositories.activity_repository import IActivityRepository
from app.infrastructure.database.models.activity import Activity
from app.schemas.activity import ActivityCreate, ActivityUpdate


class ActivityUseCases:
    def __init__(self, repository: IActivityRepository, session: AsyncSession):
        self.repository = repository
        self.session = session

    async def create_activity(
        self, user_id: UUID, activity_in: ActivityCreate
    ) -> Activity:
        activity = Activity(
            title=activity_in.title,
            description=activity_in.description,
            category_id=activity_in.category_id,
            user_id=user_id,
        )
        await self.repository.create(activity)
        await self.session.commit()
        await self.session.refresh(activity)
        return activity

    async def get_all_activities(self, user_id: UUID) -> list[Activity]:
        return await self.repository.get_all_by_user(user_id)

    async def update_activity(
        self, activity_id: UUID, user_id: UUID, activity_in: ActivityUpdate
    ) -> Activity:
        activity = await self.repository.get_by_id(activity_id, user_id)
        if not activity:
            raise AppException(
                code="ACTIVITY_NOT_FOUND",
                message="Atividade não encontrada.",
                status_code=404,
            )

        if activity_in.title is not None:
            activity.title = activity_in.title
        if activity_in.description is not None:
            activity.description = activity_in.description
        if activity_in.category_id is not None:
            activity.category_id = activity_in.category_id

        await self.repository.update(activity)
        await self.session.commit()
        await self.session.refresh(activity)
        return activity

    async def delete_activity(self, activity_id: UUID, user_id: UUID) -> None:
        activity = await self.repository.get_by_id(activity_id, user_id)
        if not activity:
            raise AppException(
                code="ACTIVITY_NOT_FOUND",
                message="Atividade não encontrada.",
                status_code=404,
            )

        await self.repository.soft_delete(activity)
        await self.session.commit()

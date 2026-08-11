from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ActivityBase(BaseModel):
    title: str
    description: str | None = None
    category_id: UUID


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category_id: UUID | None = None


class ActivityResponse(ActivityBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class MaterialBase(BaseModel):
    name: str
    url: str | None = None


class MaterialCreate(MaterialBase):
    pass


class MaterialUpdate(BaseModel):
    name: str | None = None
    url: str | None = None


class MaterialResponse(MaterialBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

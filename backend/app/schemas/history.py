from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class HistoryCreate(BaseModel):
    activity_id: UUID
    start_time: datetime
    end_time: datetime | None = None


class HistoryUpdate(BaseModel):
    start_time: datetime | None = None
    end_time: datetime | None = None


class HistoryResponse(BaseModel):
    id: UUID
    activity_id: UUID
    user_id: UUID
    start_time: datetime
    end_time: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

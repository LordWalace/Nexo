from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class BaseEntity(BaseModel):
    id: str | None = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    deleted_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class User(BaseEntity):
    email: str
    is_active: bool = True
    is_verified: bool = False


class Category(BaseEntity):
    name: str
    user_id: str


class Material(BaseEntity):
    name: str
    url: str | None = None
    user_id: str


class Activity(BaseEntity):
    title: str
    description: str | None = None
    category_id: str
    user_id: str


class ActivityMaterial(BaseEntity):
    activity_id: str
    material_id: str


class ActivityExecutionPeriod(BaseEntity):
    activity_id: str
    started_at: datetime
    paused_at: datetime | None = None
    resumed_at: datetime | None = None
    ended_at: datetime | None = None


class Notification(BaseEntity):
    user_id: str
    title: str
    body: str
    is_read: bool = False


class Device(BaseEntity):
    user_id: str
    push_token: str


class UserSession(BaseEntity):
    user_id: str
    refresh_token: str
    expires_at: datetime


class UserConsent(BaseEntity):
    user_id: str
    agreed_to_terms: bool

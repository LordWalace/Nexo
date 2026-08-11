from fastapi import APIRouter

from app.api.v1 import (
    activities,
    auth,
    categories,
    history,
    materials,
    notifications,
    statistics,
    users,
)
from app.api.v1.endpoints import health

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(categories.router)
api_router.include_router(activities.router)
api_router.include_router(materials.router)
api_router.include_router(history.router)
api_router.include_router(notifications.router)
api_router.include_router(statistics.router)

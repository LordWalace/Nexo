from fastapi import APIRouter, Depends
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.dependencies import get_db
from app.core.exceptions import AppException
from app.core.redis import get_redis

router = APIRouter()


@router.get("")
async def health_check() -> dict[str, str]:
    return {"status": "ok", "service": settings.APP_SLUG}


@router.get("/database")
async def health_check_database(db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "service": f"{settings.APP_SLUG}-db"}
    except Exception:
        raise AppException(
            status_code=503,
            code="DATABASE_UNAVAILABLE",
            message="O banco de dados está indisponível.",
        )


@router.get("/redis")
async def health_check_redis(redis: Redis = Depends(get_redis)) -> dict[str, str]:
    try:
        await redis.ping()
        return {"status": "ok", "service": f"{settings.APP_SLUG}-redis"}
    except Exception:
        raise AppException(
            status_code=503,
            code="REDIS_UNAVAILABLE",
            message="O Redis está indisponível.",
        )

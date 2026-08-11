from collections.abc import AsyncGenerator

from redis.asyncio import Redis, from_url

from app.core.config import settings

_redis_client: Redis | None = None


async def get_redis_client() -> Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = from_url(settings.REDIS_URL, decode_responses=True)
    return _redis_client


async def close_redis() -> None:
    global _redis_client
    if _redis_client is not None:
        await _redis_client.aclose()
        _redis_client = None


async def get_redis() -> AsyncGenerator[Redis, None]:
    client = await get_redis_client()
    yield client


async def ping_redis() -> bool:
    client = await get_redis_client()
    try:
        return await client.ping()
    except Exception:
        return False

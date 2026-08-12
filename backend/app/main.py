from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.core.exceptions import (
    AppException,
    app_exception_handler,
    global_exception_handler,
)
from app.core.logging import setup_logging
from app.core.redis import close_redis, get_redis_client

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI) -> "Any":
    # Startup
    await get_redis_client()
    yield
    # Shutdown
    await close_redis()


app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for Nexo",
    version="0.1.0",
    lifespan=lifespan,
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Welcome to Nexo API", "docs": "/docs"}


app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

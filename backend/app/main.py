from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.exceptions import (
    AppException,
    app_exception_handler,
    global_exception_handler,
)
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(
    title=settings.APP_NAME, description="Backend API for Nexo", version="0.1.0"
)

app.include_router(api_router)

app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

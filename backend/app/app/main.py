from fastapi import FastAPI

from app.api.api_v1.api import api_router
from app.api.sentry_endpoint import sentry_router
from app.core.sentry import init_sentry
from app.core.config import settings
from app.core.logger import init_logging
from app.core.middleware import middleware


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    middleware=middleware,
)

init_sentry()
init_logging()

app.include_router(api_router, prefix=settings.API_V1_STR)

app.include_router(sentry_router, include_in_schema=False)

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.api_v1.api import api_router
from api.sentry_endpoint import sentry_router
from core.config import settings
from core.logger import init_logging
from core.middleware import middleware
from core.sentry import init_sentry


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    middleware=middleware,
)

if settings.DEBUG:
    app.mount("/videos", StaticFiles(directory=f"{settings.DATA_LOCAL_DIR}/videos"), name="videos")

init_sentry()
# init_logging()

app.include_router(api_router, prefix=settings.API_V1_STR)

app.include_router(sentry_router, include_in_schema=False)

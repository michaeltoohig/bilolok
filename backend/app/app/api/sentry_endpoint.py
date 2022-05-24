import json
from urllib.parse import urlparse

import httpx
import loguru
from fastapi import APIRouter, Request, Response, status

from app.core.config import settings

logger = loguru.logger

sentry_router = APIRouter()


@sentry_router.post("/sentry")
async def sentry_tunnel_endpoint(request: Request):
    if settings.DEBUG:
        envelope = await request.body()
        pieces = envelope.decode().split("\n")
        # logger.error(envelope)
        return Response(status_code=status.HTTP_201_CREATED)
    try:
        envelope = await request.body()
        pieces = envelope.decode().split("\n")
        header = json.loads(pieces[0])
        dsn = urlparse(header["dsn"])
        project_id = int(dsn.path.strip("/"))
        if (
            project_id in settings.SENTRY_PROJECT_IDS
            and dsn.hostname == settings.SENTRY_HOST
        ):
            logger.debug("Sending to Sentry...")
            httpx.post(
                f"https://{settings.SENTRY_HOST}/api/{project_id}/envelope/",
                data=envelope,
            )
        else:
            logger.warning("Sentry DSN does not match expected values")
    except Exception as exc:
        logger.warning("Exception handling sentry tunnel request")
        logger.exception(exc)
        raise exc  # will be picked up by sentry_sdk
    finally:
        return Response(status_code=status.HTTP_201_CREATED)

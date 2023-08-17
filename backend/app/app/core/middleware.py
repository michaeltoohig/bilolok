import time
from typing import Any, Optional

import loguru
from fastapi import Request, Response
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.http import HTTPBearer
from starlette.middleware.base import (BaseHTTPMiddleware,
                                       RequestResponseEndpoint)
from starlette_context import context, plugins
from starlette_context.middleware import ContextMiddleware

from core.config import settings
from core.sentry import sentry_sdk
from core.users import get_jwt_strategy

logger = loguru.logger


class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        with logger.contextualize(request_id=context.data.get("X-Request-ID")):
            start_time = time.time()
            response = await call_next(request)
            message = '{client_ip}:{client_port} - "{method} {path} {scheme}/{http_version}" {status_code}'.format(
                client_ip=request.scope.get("client")[0],
                client_port=request.scope.get("client")[1],
                method=request.scope.get("method"),
                path=request.scope.get("path"),
                scheme=request.scope.get("scheme"),
                http_version=request.scope.get("http_version"),
                status_code=response.status_code,
            )
            logger.info(message)
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            logger.debug(f"Request time: {str(process_time)}")
            return response


class SentryExceptionMiddleware(BaseHTTPMiddleware):
    """Middleware to handle exceptions and pass them to Sentry"""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        with logger.contextualize(request_id=context.data.get("X-Request-ID")):
            try:
                response = await call_next(request)
                return response
            except Exception as e:
                logger.error(f"Request failed: {e}")
                with sentry_sdk.push_scope() as scope:
                    scope.set_context("request", request)
                    user_id = context.data.get("user_id", None)
                    scope.user = {
                        "ip_address": request.client.host,
                        "id": user_id,
                    }
                    sentry_sdk.capture_exception(e)
                raise e


class FastAPIUsersJWTPlugin(plugins.base.Plugin):
    """Starlette-Context middleware to collect user_id from JWT token"""

    key = "user_id"
    jwt_strategy = get_jwt_strategy()
    jwt_bearer_authorization = HTTPBearer(auto_error=False)

    async def process_request(self, request: Request) -> Optional[Any]:
        auth = await self.jwt_bearer_authorization(request)
        if not auth:
            return None
        user_id = await self.jwt_strategy.get_user_id(auth.credentials)
        return user_id


middleware = [
    Middleware(
        ContextMiddleware,
        plugins=[
            plugins.RequestIdPlugin(),
            plugins.ForwardedForPlugin(),
            FastAPIUsersJWTPlugin(),
        ],
    ),
    Middleware(SentryExceptionMiddleware),
]


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    print(settings.BACKEND_CORS_ORIGINS)
    middleware.append(
        Middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    )


# Set logging on requests for development debugging
# Probably will make this always-on in future and include
# some logging to file down the road.
if settings.DEBUG:
    middleware.append(Middleware(RequestLogMiddleware))

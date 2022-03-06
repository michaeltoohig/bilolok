from typing import Any, Optional

from fastapi import Request, Response
from fastapi.security.http import HTTPBearer
from fastapi.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette_context import context, plugins
from starlette_context.middleware import ContextMiddleware

from app.core.sentry import sentry_sdk
from app.core.users import get_jwt_strategy


class SentryExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            response = await call_next(request)
            return response
        except Exception as e:
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
    key = "user_id"
    jwt_strategy = get_jwt_strategy()
    jwt_bearer_authorization = HTTPBearer(auto_error=False)

    async def process_request(
        self, request: Request
    ) -> Optional[Any]:
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
            FastAPIUsersJWTPlugin()
        ]
    ),
    Middleware(SentryExceptionMiddleware)
]
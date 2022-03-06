from typing import Any, Optional

from fastapi import Request
from fastapi.security.http import HTTPBearer
from fastapi.middleware import Middleware
from starlette_context import plugins
from starlette_context.middleware import ContextMiddleware

from app.core.users import get_jwt_strategy


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
    )
]
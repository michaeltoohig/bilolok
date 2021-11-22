from typing import Any
from fastapi import Response, Depends

from app.core.config import settings
from app.core.users import fastapi_users, jwt_authentication


auth_router = fastapi_users.get_auth_router(jwt_authentication)
register_router = fastapi_users.get_register_router()
reset_password_router = fastapi_users.get_reset_password_router()
verify_router = fastapi_users.get_verify_router()


# @auth_router.post("/refresh")
# async def refresh_jwt(
#     response: Response,
#     user=Depends(fastapi_users.current_user(active=True)),
# ) -> Any:
#     return await jwt_authentication.get_login_response(user, response)

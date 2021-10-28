from app.api.tasks import on_after_register, on_after_forgot_password, after_verification_request
from app.core.config import settings
from app.core.security import jwt_authentication
from app.core.users import fastapi_users


register_router = fastapi_users.get_register_router(on_after_register)
reset_password_router = fastapi_users.get_reset_password_router(settings.SECRET_KEY, after_forgot_password=on_after_forgot_password)
verify_router = fastapi_users.get_verify_router(settings.SECRET_KEY, after_verification_request=after_verification_request)
auth_router = fastapi_users.get_auth_router(jwt_authentication)

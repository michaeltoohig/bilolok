from fastapi_users.authentication import JWTAuthentication

from app.core.config import settings


jwt_authentication = JWTAuthentication(
    secret=settings.SECRET_KEY,
    lifetime_seconds=3600,
    tokenUrl="/api/v1/auth/jwt/login",
    token_audience=[f"{settings.PROJECT_SLUG}:auth"]
)
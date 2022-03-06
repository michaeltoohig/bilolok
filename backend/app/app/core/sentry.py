import sentry_sdk
from app.core.config import settings


sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
)
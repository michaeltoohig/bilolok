import sentry_sdk
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from app.core.config import settings


def traces_sampler(sampling_context):
    if settings.DEBUG:
        # Drop this transaction
        return 0
    else:
        # Send 100% of all events
        return 1


def init_sentry():
    if settings.DEBUG:
        return None
    else:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            integrations=[
                SqlalchemyIntegration(),
            ],
            traces_sampler=traces_sampler,
        )

# So this nonsense here is due to an error in uvicorn
# asyncio.exceptions.CancelledError is thrown whenever the app
# is stopped `ctrl+c` which is sending the error to sentry from
# development constantly. `traces_sampler` hook does not catch
# this exception because it is happening outside of FastAPI in uvicorn. 
# https://github.com/encode/uvicorn/issues/1160
# https://github.com/encode/starlette/issues/486
init_sentry()
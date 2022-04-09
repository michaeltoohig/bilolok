import sentry_sdk
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from app.core.config import settings

# def traces_sampler(sampling_context):
#     if settings.DEBUG:
#         # Drop this transaction
#         return 0
#     else:
#         # Set to 1.0 to capture 100%
#         # of transactions for performance monitoring.
#         # We recommend adjusting this value in production
#         return 1


def init_sentry():
    # So this here is due to an error in uvicorn
    # asyncio.exceptions.CancelledError is thrown whenever the app
    # is stopped `ctrl+c` which is sending the error to sentry from
    # development constantly. `traces_sampler` hook does not catch
    # this exception because it is happening outside of FastAPI in uvicorn.
    # https://github.com/encode/uvicorn/issues/1160
    # https://github.com/encode/starlette/issues/486
    if settings.DEBUG:
        return None
    else:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            integrations=[
                SqlalchemyIntegration(),
            ],
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production
            traces_sample_rate=0.05,
            # traces_sampler=traces_sampler,
        )

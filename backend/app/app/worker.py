# isort:skip_file

# import sys

# sys.path.extend(["./"])

# TODO debug this issue we are seeing https://github.com/aio-libs/aioredis-py/issues/878

from pydantic.utils import import_string

from app.db.session import SessionLocal
from app.core.arq_app import redis_settings


ARQ_BACKGROUND_FUNCTIONS = [
    "app.tasks.utils.test_arq",
    "app.tasks.utils.test_arq_subtask",
    "app.tasks.utils.send_daily_push_notification",
]


FUNCTIONS: list = (
    [
        import_string(background_function)
        for background_function in list(ARQ_BACKGROUND_FUNCTIONS)
    ]
    if ARQ_BACKGROUND_FUNCTIONS is not None
    else list()
)


async def startup(ctx):
    """
    Binds a connection set to the db object.
    """
    ctx["db"] = SessionLocal()


async def shutdown(ctx):
    """
    Pops the bind on the db object.
    """
    ctx["db"].close()


class WorkerSettings:
    """
    Settings for the ARQ worker.
    """

    # NOTE cron times must be in UTC (hour=6 == 6:00 UTC == 17:00 VUT)
    # XXX https://github.com/samuelcolvin/arq/issues/304 before uncommenting cron_jobs
    # cron_jobs = [
    #     cron(
    #         "app.tasks.utils.send_daily_push_notification",
    #         weekday={0, 1, 2, 3, 4, 5},
    #         hour=6,
    #         minute=0,
    #     ),
    # ]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = redis_settings
    functions: list = FUNCTIONS

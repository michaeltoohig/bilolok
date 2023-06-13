# isort:skip_file

# import sys

# sys.path.extend(["./"])

# TODO debug this issue we are seeing https://github.com/aio-libs/aioredis-py/issues/878

from pydantic.utils import import_string
from arq import cron

from db.session import async_session
from core.arq_app import redis_settings

# HACK handling circular import issues by importing these at the top of the worker
from models.user import User  # noqa
from schemas.user import UserSchema  # noqa


ARQ_BACKGROUND_FUNCTIONS = [
    "app.tasks.utils.test_arq",
    "app.tasks.utils.test_arq_subtask",
    "app.tasks.utils.daily_send_push_notification",
    "app.tasks.nakamal.select_featured_nakamal",
    "app.tasks.nakamal.update_nakamal_chief",
    "app.tasks.nakamal.daily_check_chief",
    "app.tasks.video.process_video",
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
    ctx["db_session"] = async_session


async def shutdown(ctx):
    """
    Pops the bind on the db object.
    """
    pass


class WorkerSettings:
    """
    Settings for the ARQ worker.
    """

    # NOTE cron times must be in UTC (hour=6 == 6:00 UTC == 17:00 VUT)
    HOUR_MIDNIGHT = 13
    # XXX https://github.com/samuelcolvin/arq/issues/304 before uncommenting cron_jobs
    cron_jobs = [
        cron(
            "app.tasks.utils.daily_send_push_notification",
            weekday={0, 1, 2, 3, 4, 5},
            hour=6,
            minute=0,
        ),
        cron(
            "app.tasks.nakamal.select_featured_nakamal",
            hour=HOUR_MIDNIGHT,
            minute=0,
            run_at_startup=True,  # our redis is currently not persistent so we need to run this at startup
        ),
        cron(
            "app.tasks.nakamal.daily_check_chief",
            hour=HOUR_MIDNIGHT,
            minute=0,
        )
    ]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = redis_settings
    functions: list = FUNCTIONS
    max_jobs = 1
    poll_delay = 5

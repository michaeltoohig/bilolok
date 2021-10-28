# isort:skip_file

# import sys

# sys.path.extend(["./"])

# TODO debug this issue we are seeing https://github.com/aio-libs/aioredis-py/issues/878

from arq import cron
from pydantic.utils import import_string

from app.db.session import SessionLocal
from app.core.arq_app import redis_settings


ARQ_BACKGROUND_FUNCTIONS = [
    "app.tasks.utils.test_arq",
]


FUNCTIONS: list = [
    import_string(background_function)
    for background_function in list(ARQ_BACKGROUND_FUNCTIONS)
] if ARQ_BACKGROUND_FUNCTIONS is not None else list()


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

    # cron_jobs = [
    #     cron("app.tasks.", second=30),
    #     cron("app.tasks."),
    # ]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = redis_settings
    functions: list = FUNCTIONS

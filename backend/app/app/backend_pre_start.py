import logging
from pathlib import Path

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from core.config import settings
from db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1

import redis


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init_db() -> None:
    try:
        db = SessionLocal()
        # Try to create session to check if DB is awake
        db.execute("SELECT 1")
    except Exception as e:
        logger.error(e)
        raise e


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init_redis() -> None:
    try:
        # Try to create session to check if Redis is awake
        r = redis.Redis(host=settings.REDIS_SERVER, port=settings.REDIS_PORT, db=0)
        assert r.ping()
    except Exception as e:
        logger.error(e)
        raise e


def init_directories() -> None:
    images = Path(settings.IMAGES_LOCAL_DIR)
    try:
        # Try to check and create directory
        if not images.exists():
            images.mkdir()
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Initializing service")
    init_db()
    init_redis()
    logger.info("Service finished initializing")
    init_directories()
    logger.info("Local directories exist")


if __name__ == "__main__":
    main()

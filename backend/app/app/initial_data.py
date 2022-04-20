import asyncio
import logging

from app.db.init_db import init_db
from app.db.session import async_engine, async_session


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init() -> None:
    async with async_engine.begin() as connection:
        async with async_session(bind=connection) as session:
            await init_db(session)
            await session.flush()
            await session.rollback()


async def main() -> None:
    logger.info("Creating initial data")
    await init()
    logger.info("Initial data created")


if __name__ == "__main__":
    asyncio.run(main())

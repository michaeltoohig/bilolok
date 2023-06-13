from typing import AsyncIterator

from aioredis import create_redis_pool, Redis
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from db.session import async_session


async def get_db() -> AsyncSession:
    """
    Dependency function that yields db sessions
    """
    async with async_session() as session:
        yield session
        await session.commit()


async def get_redis() -> AsyncIterator[Redis]:
    """
    Dependency function that yeilds redis pool
    """
    pool = await create_redis_pool(f"redis://{settings.REDIS_SERVER}:{settings.REDIS_PORT}")
    yield pool
    pool.close()
    await pool.wait_closed()
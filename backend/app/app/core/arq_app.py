from arq.connections import ArqRedis, RedisSettings, create_pool

from app.core.config import settings

redis_settings = RedisSettings(host=settings.REDIS_SERVER, port=settings.REDIS_PORT)


async def get_arq_app():
    arq_app: ArqRedis = await create_pool(redis_settings)
    return arq_app

import random

from app.crud.nakamal import CRUDNakamal


async def select_featured_nakamal(ctx: dict):
    redis = ctx["redis"]
    db_session = ctx["db_session"]
    async with db_session() as db:
        crud_nakamal = CRUDNakamal(db)
        nakamals = await crud_nakamal.get_multi()
        nakamal_ids = map(lambda n: n.id, nakamals)
        featured_id = random.choice(list(nakamal_ids))
        await redis.set("featured-nakamal", str(featured_id))
        await db.commit()

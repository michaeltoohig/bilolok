from datetime import datetime, timedelta, timezone
import random

from crud.nakamal import CRUDNakamal
from crud.checkin import CRUDCheckin


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


async def update_nakamal_chief(ctx: dict, nakamal_id: str):
    db_session = ctx["db_session"]
    async with db_session() as db:
        crud_nakamal = CRUDNakamal(db)
        nakamal = await crud_nakamal.get_by_id(nakamal_id)
        if not nakamal:
            return "Nakamal does not exist."
        crud_checkin = CRUDCheckin(db)
        chief_id = await crud_checkin.calculate_chief_of_nakamal(nakamal.id)
         
        if nakamal.chief is not None and nakamal.chief.id == chief_id:
            return "Nakamal chief does not change."
        else:
            if nakamal.chief is not None:
                previous_chief_id = nakamal.chief.id
                # TODO send alert to user who lost position
            await crud_nakamal.update_chief(nakamal.id, chief_id)
            # TODO send alert to chief and add timeline event


async def daily_check_chief(ctx: dict):
    arq_app = ctx["redis"]
    db_session = ctx["db_session"]
    async with db_session() as db:
        crud_checkin = CRUDCheckin(db)
        now = datetime.utcnow()
        end = now.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
        start = end - timedelta(days=30)
        nakamal_ids = await crud_checkin._get_unique_nakamals_between(start=start, end=end)
        if len(nakamal_ids) == 0:
            return "No check-ins during date range."
        for nakamal_id in nakamal_ids:
            await arq_app.enqueue_job("update_nakamal_chief", str(nakamal_id))

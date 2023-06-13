from sqlalchemy.ext.asyncio import AsyncSession

from models.nakamal import NakamalArea, NakamalKavaSource, Province
from schemas.nakamal import NakamalAreaSchemaIn, NakamalKavaSourceSchemaIn
from tests.utils.utils import random_lower_string


async def create_random_kava_source(db_session: AsyncSession):
    island = random_lower_string()
    province = Province.UNDEFINED
    kava_source_in = NakamalKavaSourceSchemaIn(island=island, province=province)
    kava_source = NakamalKavaSource(**kava_source_in.dict())
    db_session.add(kava_source)
    await db_session.commit()
    await db_session.refresh(kava_source)
    return kava_source


async def create_random_area(db_session: AsyncSession):
    name = random_lower_string()
    area_in = NakamalAreaSchemaIn(name=name)
    area = NakamalArea(**area_in.dict())
    db_session.add(area)
    await db_session.commit()
    await db_session.refresh(area)
    return area

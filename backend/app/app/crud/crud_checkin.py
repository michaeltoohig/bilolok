from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, Union, List
from fastapi_crudrouter.core.databases import pydantify_record

from sqlalchemy import desc, and_

from app.crud.base import CRUDBase
from app.db.session import database
from app.models.checkin import Checkin, CheckinTable
from app.schemas.checkin import CheckinCreate, CheckinDB, CheckinUpdate
from pydantic.types import UUID4


class CRUDCheckin(CRUDBase[Checkin, CheckinCreate, CheckinUpdate]):
    async def get_multi_by_nakamal(self, nakamal_id: UUID4, *, skip: int = 0, limit: int = 100) -> List[Checkin]:
        query = self.model.select() \
            .where(self.model.c.nakamal_id == nakamal_id) \
            .order_by(desc(self.model.c.created_at)) \
            .offset(skip).limit(limit)
        checkins = pydantify_record(await database.fetch_all(query))
        return checkins
    
    async def get_last_by_user(self, user_id: UUID4, *, nakamal_id: Optional[UUID4] = None) -> Optional[Checkin]:
        query = self.model.select() \
            .where(self.model.c.user_id == user_id) \
            .order_by(desc(self.model.c.created_at))
        if nakamal_id:
            query= query.where(self.model.c.nakamal_id == nakamal_id)
        record = await database.fetch_one(query)
        if record:
            return pydantify_record(record)
        return None

    async def get_recent_by_nakamal(self, nakamal_id: UUID4, *, user_id: Optional[UUID4] = None) -> List[Checkin]:
        threshold = datetime.now(tz=timezone.utc) - timedelta(hours=6)  # XXX hardcoded value
        query = self.model.select() \
            .where(self.model.c.nakamal_id == nakamal_id) \
            .where(self.model.c.created_at >= threshold) \
            .order_by(desc(self.model.c.created_at))
            # .offset(skip) \
            # .limit(limit)
        if user_id:
            query = query.where(self.model.c.user_id == user_id)
        records = await database.fetch_all(query)
        return pydantify_record(records)


checkin = CRUDCheckin(CheckinTable)

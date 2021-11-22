from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, Union, List
from uuid import UUID

from fastapi_crudrouter.core.databases import pydantify_record
from sqlalchemy import desc, and_, select

from app import models
from app.crud.base import CRUDBase
from app.db.session import database
# from app.models.checkin import Checkin, CheckinTable
# from app.schemas.checkin import CheckinCreate, models.Checkin, CheckinUpdate
# from pydantic.types import UUID


# TODO update to use ormar

class CRUDCheckin(CRUDBase[models.Checkin]):
    async def get(self, id: Any) -> Optional[models.Checkin]:
        query = (
            self.model.select()
            .join(models.user)
            .where(self.model.c.id == id)
        )
        record = await database.fetch_one(query)
        if record:
            return pydantify_record(record)
        return None
    
    async def get_multi_by_nakamal(self, nakamal_id: UUID, *, skip: int = 0, limit: int = 100, exclude_private: bool = True) -> List[models.Checkin]:
        j = self.model.join(models.User)
        query = (
            select([self.model, models.User])
            .select_from(j)
            .where(
                and_(
                    self.model.c.nakamal_id == nakamal_id,
                )
            )
            .order_by(desc(self.model.c.created_at))
            .offset(skip).limit(limit)
        )
        if exclude_private:
            query = query.where(self.model.c.private == False)
        checkins = pydantify_record(await database.fetch_all(query))
        import pdb; pdb.set_trace()
        
        return checkins
    
    async def get_last_by_user(self, user_id: UUID, *, nakamal_id: Optional[UUID] = None, exclude_private: bool = True) -> Optional[models.Checkin]:
        query = (
            self.model.select()
            .where(
                and_(
                    self.model.c.user_id == user_id,
                )
            )
            .order_by(desc(self.model.c.created_at))
        )
        if exclude_private:
            query = query.where(self.model.c.private == False)
        if nakamal_id:
            query= query.where(self.model.c.nakamal_id == nakamal_id)
        record = await database.fetch_one(query)
        if record:
            return pydantify_record(record)
        return None

    async def get_recent_by_nakamal(self, nakamal_id: UUID, *, user_id: Optional[UUID] = None, exclude_private: bool = True) -> List[models.Checkin]:
        threshold = datetime.now(tz=timezone.utc) - timedelta(hours=6)  # XXX hardcoded value
        query = (
            self.model.select()
            .where(
                and_(
                    self.model.c.nakamal_id == nakamal_id,
                    self.model.c.created_at >= threshold,
                )
            )
            .order_by(desc(self.model.c.created_at))
            # .offset(skip).limit(limit)
        )
        if exclude_private:
            query = query.where(self.model.c.private == False)
        if user_id:
            query = query.where(self.model.c.user_id == user_id)
        records = await database.fetch_all(query)
        return pydantify_record(records)


checkin = CRUDCheckin(models.Checkin)

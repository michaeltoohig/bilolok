from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, Union, List
from uuid import UUID

from ormar.exceptions import NoMatch

from app import models
from app.crud.base import CRUDBase
from app.db.session import database
# from app.models.checkin import Checkin, CheckinTable
# from app.schemas.checkin import CheckinCreate, models.Checkin, CheckinUpdate
# from pydantic.types import UUID


class CRUDCheckin(CRUDBase[models.Checkin]):
    async def _get_one(self, **kwargs: Any) -> Optional[models.Checkin]:
        try:
            item = await self.model.objects.filter(**kwargs).get()
        except NoMatch:
            return None
        return item
    
    async def _get_multi(self, skip: int = 0, limit: int = 20, **kwargs: Any) -> List[models.Checkin]:
        return await self.model.objects.filter(**kwargs).offset(skip).limit(limit).all()
    
    async def get_multi_by_nakamal(self, nakamal_id: UUID, *, skip: int = 0, limit: int = 100) -> List[models.Checkin]:
        params = dict(nakamal=nakamal_id, private=False)
        return await self._get_multi(skip, limit, **params)
    
    # async def get_recent_by_nakamal(self, nakamal_id: UUID, *, user_id: Optional[UUID] = None) -> List[models.Checkin]:
    #     params = dict(nakamal=nakamal_id, private=False)
    #     threshold = datetime.now(tz=timezone.utc) - timedelta(hours=6)  # XXX hardcoded value
    #     query = (
    #         self.model.select()
    #         .where(
    #             and_(
    #                 self.model.c.nakamal_id == nakamal_id,
    #                 self.model.c.created_at >= threshold,
    #             )
    #         )
    #         .order_by(desc(self.model.c.created_at))
    #         # .offset(skip).limit(limit)
    #     )
    #     if exclude_private:
    #         query = query.where(self.model.c.private == False)
    #     if user_id:
    #         query = query.where(self.model.c.user_id == user_id)
    #     records = await database.fetch_all(query)
    #     return pydantify_record(records)

    async def get_multi_by_user(self, user_id: UUID, *, skip: int = 0, limit: int = 100, exclude_private: bool = True, **kwargs) -> List[models.Checkin]:
        params = dict(user=user_id, **kwargs)
        if exclude_private:
            params["private"] = False
        return await self._get_multi(skip, limit, **params)

    async def get_last_by_user(self, user_id: UUID, *, nakamal_id: Optional[UUID] = None, exclude_private: bool = True) -> Optional[models.Checkin]:
        params = dict(user=user_id)
        if nakamal_id:
            params["nakamal"] = nakamal_id
        if exclude_private:
            params["private"] = False
        try:
            item = await self.model.objects.filter(**params).first()
            return item
        except NoMatch:
            return None



checkin = CRUDCheckin(models.Checkin)

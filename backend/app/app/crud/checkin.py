
from typing import Optional, List, Type
from uuid import UUID

from sqlalchemy import desc, select, and_

from app import models
from app.crud.base import CRUDBase
from app.models.checkin import Checkin
from app.schemas.checkin import CheckinSchemaIn, CheckinSchema


class CRUDCheckin(CRUDBase[Checkin, CheckinSchemaIn, CheckinSchema]):
    @property
    def _in_schema(self) -> Type[CheckinSchemaIn]:
        return CheckinSchemaIn

    @property
    def _schema(self) -> Type[CheckinSchema]:
        return CheckinSchema

    @property
    def _table(self) -> Type[Checkin]:
        return Checkin
    
    async def get_multi_by_nakamal(self, nakamal_id: UUID, *, skip: int = 0, limit: int = 100) -> List[CheckinSchema]:
        stmt = (
            select(self._table)
            .where(
                and_(
                    self._table.nakamal_id == nakamal_id,
                    self._table.private == False,
                )
            )
        )
        stmt.order_by(desc(self._table.created_at))
        items = await self._db_session.execute(stmt)
        return (self._schema.from_orm(item) for item in items)
        
    # async def get_recent_by_nakamal(self, nakamal_id: UUID, *, user_id: Optional[UUID] = None) -> List[CheckinSchema]:
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

    async def get_multi_by_user(self, user_id: UUID, *, skip: int = 0, limit: int = 100, exclude_private: bool = True, **kwargs) -> List[CheckinSchema]:
        stmt = (
            select(self._table)
            .where(self._table.user_id == user_id)
        )
        if exclude_private:
            stmt.where(self._table.private == False)
        stmt.order_by(desc(self._table.created_at))
        items = await self._db_session.execute(stmt)
        return (self._schema.from_orm(item) for item in items)

    async def get_last_by_user(self, user_id: UUID, *, nakamal_id: Optional[UUID] = None, exclude_private: bool = True) -> Optional[CheckinSchema]:
        stmt = (
            select(self._table)
            .where(self._table.user_id == user_id)
        )
        if nakamal_id:
            stmt.where(self._table.nakamal_id == nakamal_id)
        if exclude_private:
            stmt.where(self._table.private == False)
        stmt.order_by(desc(self._table.created_at))
        stmt.limit(1)
        item = await self._db_session.execute(stmt)
        import pdb; pdb.set_trace()
        
        return self._schema.from_orm(item)

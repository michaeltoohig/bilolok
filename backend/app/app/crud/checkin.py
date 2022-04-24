from datetime import datetime, timedelta, timezone
from typing import List, Optional, Type
from uuid import UUID, uuid4
from app.db.errors import DoesNotExist

from sqlalchemy import and_, desc, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models.checkin import Checkin
from app.schemas.checkin import CheckinSchema, CheckinSchemaIn


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

    async def _get_one(self, item_id: UUID):
        query = (
            select(self._table)
            .options(selectinload(self._table.nakamal))
            .where(self._table.id == item_id)
        )
        try:
            (item,) = (await self._db_session.execute(query)).one()
        except NoResultFound:
            item = None
        return item

    async def create(
        self, in_schema: CheckinSchemaIn, *, user_id: UUID
    ) -> CheckinSchema:
        item_id = uuid4()
        item = self._table(id=item_id, **in_schema.dict(), user_id=user_id)
        self._db_session.add(item)
        await self._db_session.commit()
        return await self.get_by_id(item_id)

    async def get_multi(
        self, *, skip: int = 0, limit: int = 100
    ) -> List[CheckinSchema]:
        query = (
            select(self._table)
            .options(selectinload(self._table.nakamal))
            .order_by(desc(self._table.created_at))
            .offset(skip)
            .limit(limit)
        )
        results = await self._db_session.execute(query)
        return (self._schema.from_orm(item) for item in results.scalars())

    async def get_recent(self) -> List[CheckinSchema]:
        threshold = datetime.now(tz=timezone.utc) - timedelta(
            hours=3
        )  # XXX hardcoded value
        query = (
            select(self._table)
            .where(self._table.created_at >= threshold)
            .options(selectinload(self._table.nakamal))
            .options(selectinload(self._table.user))
            .order_by(desc(self._table.created_at))
        )
        results = await self._db_session.execute(query)
        return (self._schema.from_orm(item) for item in results.scalars())

    async def get_multi_by_nakamal(
        self, nakamal_id: UUID, *, skip: int = 0, limit: int = 100
    ) -> List[CheckinSchema]:
        query = (
            select(self._table)
            .options(selectinload(self._table.nakamal))
            .where(
                and_(
                    self._table.nakamal_id == nakamal_id,
                    self._table.private == False,
                )
            )
            .order_by(desc(self._table.created_at))
        )
        results = await self._db_session.execute(query)
        return (self._schema.from_orm(item) for item in results.scalars())

    async def get_multi_by_user(
        self,
        user_id: UUID,
        *,
        skip: int = 0,
        limit: int = 100,
        nakamal_id: Optional[UUID] = None,
        exclude_private: bool = True
    ) -> List[CheckinSchema]:
        query = (
            select(self._table)
            .options(selectinload(self._table.nakamal))
            .where(self._table.user_id == user_id)
        )
        if nakamal_id:
            query = query.where(self._table.nakamal_id == nakamal_id)
        if exclude_private:
            query = query.where(self._table.private == False)
        query = query.order_by(desc(self._table.created_at))
        results = await self._db_session.execute(query)
        return (self._schema.from_orm(item) for item in results.scalars())

    async def get_last_by_user(
        self,
        user_id: UUID,
        *,
        nakamal_id: Optional[UUID] = None,
        exclude_private: bool = True
    ) -> Optional[CheckinSchema]:
        query = (
            select(self._table)
            .options(selectinload(self._table.nakamal))
            .where(self._table.user_id == user_id)
        )
        if nakamal_id:
            query = query.where(self._table.nakamal_id == nakamal_id)
        if exclude_private:
            query = query.where(self._table.private == False)
        query = query.order_by(desc(self._table.created_at))
        result = await self._db_session.execute(query)
        item = result.scalars().first()
        if not item:
            return None
        return self._schema.from_orm(item)

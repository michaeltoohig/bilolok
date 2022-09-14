from datetime import datetime, timedelta, timezone
from typing import List, Optional, Type
from uuid import UUID, uuid4

from sqlalchemy import and_, desc, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.crud.base import CRUDBase
from app.models.trip import Trip
from app.schemas.trip import TripSchema, TripSchemaIn


class CRUDTrip(CRUDBase[Trip, TripSchemaIn, TripSchema]):
    @property
    def _in_schema(self) -> Type[TripSchemaIn]:
        return TripSchemaIn

    @property
    def _schema(self) -> Type[TripSchema]:
        return TripSchema

    @property
    def _table(self) -> Type[Trip]:
        return Trip

    async def _get_one(self, item_id: UUID):
        query = (
            select(self._table)
            .options(selectinload(self._table.nakamal))
            .options(selectinload(self._table.user))
            .where(self._table.id == item_id)
        )
        try:
            (item,) = (await self._db_session.execute(query)).one()
        except NoResultFound:
            item = None
        return item

    async def create(
        self, in_schema: TripSchemaIn, *, user_id: UUID
    ) -> TripSchema:
        item_id = uuid4()
        start_at = in_schema.data[0].at
        end_at = in_schema.data[-1].at
        nakamal_id = in_schema.nakamal_id
        data = list(map(
            lambda x: dict(lat=x.lat, lng=x.lng, at=x.at.isoformat()),
            in_schema.data,
        ))
        item = self._table(
            id=item_id,
            start_at=start_at,
            end_at=end_at,
            data=data,
            nakamal_id=nakamal_id,
            user_id=user_id,
        )
        self._db_session.add(item)
        await self._db_session.commit()
        return await self.get_by_id(item_id)

    async def get_multi(
        self, *, skip: int = 0, limit: int = 100
    ) -> List[TripSchema]:
        query = (
            select(self._table)
            .options(selectinload(self._table.nakamal))
            .options(selectinload(self._table.user))
            .order_by(desc(self._table.created_at))
            .offset(skip)
            .limit(limit)
        )
        results = await self._db_session.execute(query)
        return (self._schema.from_orm(item) for item in results.scalars())

    async def get_recent(self) -> TripSchema:
        threshold = datetime.now(tz=timezone.utc) - timedelta(hours=settings.RECENT_THRESHOLD_HOURS)
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
    ) -> List[TripSchema]:
        query = (
            select(self._table)
            .options(selectinload(self._table.nakamal))
            .options(selectinload(self._table.user))
            .where(self._table.nakamal_id == nakamal_id)
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
    ) -> List[TripSchema]:
        query = (
            select(self._table)
            .options(selectinload(self._table.nakamal))
            .options(selectinload(self._table.user))
            .where(self._table.user_id == user_id)
        )
        if nakamal_id:
            query = query.where(self._table.nakamal_id == nakamal_id)
        query = query.order_by(desc(self._table.created_at))
        results = await self._db_session.execute(query)
        return (self._schema.from_orm(item) for item in results.scalars())
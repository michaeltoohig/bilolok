from datetime import datetime, timedelta, timezone
from typing import List, Optional, Type
from uuid import UUID, uuid4

from sqlalchemy import and_, desc, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload

from app.core.config import settings
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

    async def _get_unique_nakamals_between(self, *, start: datetime, end: datetime) -> List[UUID]:
        """Return list of nakamals that had one or more checkins during the given datetime range"""
        query = (
            select(self._table.nakamal_id).distinct()
            .where(
                and_(
                    self._table.created_at >= start,
                    self._table.created_at < end,
                )
            )
        )
        results = await self._db_session.execute(query)
        return list(results.scalars())

    async def get_recent(self) -> List[CheckinSchema]:
        threshold = datetime.now(tz=timezone.utc) - timedelta(
            hours=settings.RECENT_THRESHOLD_HOURS
        )
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

    async def calculate_chief_of_nakamal(self, nakamal_id: UUID, *, dt: datetime = None):
        if dt is None:
            dt = datetime.utcnow().replace(tzinfo=timezone.utc)
        threshold = dt - timedelta(days=30)
        query = (
            select(self._table)
            .options(selectinload(self._table.nakamal))
            .where(self._table.private == False)
            .where(self._table.nakamal_id == nakamal_id)
            .where(
                and_(
                    self._table.created_at >= threshold,
                    self._table.created_at < dt,
                )
            )
        )
        results = await self._db_session.execute(query)
        checkins = [self._schema.from_orm(item) for item in results.scalars()]
        if len(checkins) == 0:
            return None
        # TODO clean up once I decide how to count most checkins by a user
        from collections import Counter
        checkin_counts = Counter([c.user.id for c in checkins])
        top_count = checkin_counts.most_common(1)[0][1]
        top_user_ids = [user_id for user_id, count in checkin_counts.items() if count == top_count]
        if len(top_user_ids) > 1:
            top_user_checkins = filter(checkins, lambda i: i.user_id in top_user_ids)
            chief_id = max(top_user_checkins, key=lambda i: i.created_at)
        else:
            chief_id = top_user_ids[0]
        return chief_id
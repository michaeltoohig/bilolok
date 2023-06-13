from typing import List, Type
from uuid import UUID, uuid4

from sqlalchemy import and_, select
from sqlalchemy.exc import NoResultFound

from crud.base import CRUDBase
from models.subscription import Subscription
from schemas.subscription import SubscriptionSchema, SubscriptionSchemaIn


class CRUDSubscription(
    CRUDBase[Subscription, SubscriptionSchemaIn, SubscriptionSchema]
):
    @property
    def _in_schema(self) -> Type[SubscriptionSchemaIn]:
        return SubscriptionSchemaIn

    @property
    def _schema(self) -> Type[SubscriptionSchema]:
        return SubscriptionSchema

    @property
    def _table(self) -> Type[Subscription]:
        return Subscription

    async def create(
        self, in_schema: SubscriptionSchemaIn, *, user_id: UUID
    ) -> SubscriptionSchema:
        item_id = uuid4()
        item = self._table(id=item_id, **in_schema.dict(), user_id=user_id)
        self._db_session.add(item)
        await self._db_session.commit()
        return await self.get_by_id(item_id)

    async def find_by_device_id(
        self, device_id: str, *, user_id: UUID
    ) -> SubscriptionSchema:
        query = select(self._table).filter(
            and_(
                self._table.device_id == device_id,
                self._table.user_id == user_id,
            )
        )
        try:
            item = (await self._db_session.execute(query)).scalar_one()
        except NoResultFound:
            item = None
        return item

    async def find_multi_by_user_id(self, user_id: UUID) -> List[SubscriptionSchema]:
        query = select(self._table).filter(self._table.user_id == user_id)
        results = await self._db_session.execute(query)
        return (self._schema.from_orm(item) for item in results.scalars())

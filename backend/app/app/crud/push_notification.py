from typing import Any, Dict, List, Type
from uuid import uuid4, UUID

from sqlalchemy import and_, select
from sqlalchemy.exc import NoResultFound

from app.crud.base import CRUDBase
from app.models.push_notification import PushNotification, PushNotificationStatus
from app.schemas.push_notification import PushNotificationSchemaIn, PushNotificationSchema


class CRUDPushNotification(CRUDBase[PushNotification, PushNotificationSchemaIn, PushNotificationSchema]):    
    @property
    def _in_schema(self) -> Type[PushNotificationSchemaIn]:
        return PushNotificationSchemaIn

    @property
    def _schema(self) -> Type[PushNotificationSchema]:
        return PushNotificationSchema

    @property
    def _table(self) -> Type[PushNotification]:
        return PushNotification

    # async def find_multi_by_user_id(self, user_id: UUID) -> List[PushNotificationSchema]:
    #     query = (
    #         select(self._table)
    #         .filter(self._table.user_id == user_id)
    #     )
    #     results = await self._db_session.execute(query)
    #     return (self._schema.from_orm(item) for item in results.scalars())

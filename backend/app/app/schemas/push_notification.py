import uuid
from typing import Any, Dict, Optional

from models.push_notification import PushNotificationStatus

from .base import BaseSchema


class PushNotificationSchemaBase(BaseSchema):
    pass


class PushNotificationSchemaUpdate(BaseSchema):
    status: PushNotificationStatus
    error_data: Optional[Dict[str, Any]] = None


class PushNotificationSchemaIn(PushNotificationSchemaBase):
    user_id: uuid.UUID
    device_id: str
    data: Dict[str, Any]


class PushNotificationSchema(PushNotificationSchemaBase):
    id: uuid.UUID
    user_id: uuid.UUID
    status: PushNotificationStatus
    data: Dict[str, Any]
    # created_at: datetime
    # seen_at: Optional[datetime] = None
    # clicked_at: Optional[datetime] = None


class PushNotificationSchemaOut(PushNotificationSchema):
    pass

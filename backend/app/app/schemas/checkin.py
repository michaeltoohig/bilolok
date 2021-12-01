from typing import Optional
from datetime import datetime
import uuid

from .base import BaseSchema
from .nakamal import NakamalSchema
from .user import UserSchema


class CheckinSchemaBase(BaseSchema):
    private: Optional[bool] = False
    message: Optional[str] = None


# class CheckinUpdate(CheckinSchemaBase):
#     pass


class CheckinSchemaIn(CheckinSchemaBase):
    lat: Optional[float] = None
    lng: Optional[float] = None
    nakamal_id: uuid.UUID


class CheckinSchema(CheckinSchemaBase):
    id: uuid.UUID
    created_at: datetime
    user: UserSchema
    nakamal: NakamalSchema


class CheckinSchemaOut(CheckinSchema):
    pass

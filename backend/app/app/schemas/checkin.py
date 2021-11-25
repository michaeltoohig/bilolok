from typing import Optional
from datetime import datetime
import uuid

from .base import BaseSchema
from .nakamal import NakamalSchema


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

    user_id: uuid.UUID  # TODO UserSchema
    nakamal: NakamalSchema


class CheckinSchemaOut(CheckinSchema):
    pass

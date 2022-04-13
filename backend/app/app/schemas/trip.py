from typing import List, Tuple
import uuid
from datetime import datetime

from .base import BaseSchema
from .nakamal import NakamalSchema
from .user import UserSchema


class TripDataPoint(BaseSchema):
    lat: float
    lng: float
    at: datetime


class TripSchemaBase(BaseSchema):
    pass


class TripSchemaIn(TripSchemaBase):
    data: List[TripDataPoint]
    nakamal_id: uuid.UUID


class TripSchema(TripSchemaBase):
    id: uuid.UUID
    start_at: datetime
    end_at: datetime
    data: List[TripDataPoint]

    user: UserSchema
    nakamal: NakamalSchema


class TripSchemaOut(TripSchema):
    pass

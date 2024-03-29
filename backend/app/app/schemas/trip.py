from typing import List, Tuple
import uuid
from datetime import datetime

from pydantic import conlist

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
    data: conlist(TripDataPoint, min_items=3)  # error of empty data arrays happening. not best solution yet.
    nakamal_id: uuid.UUID


class TripSchema(TripSchemaBase):
    id: uuid.UUID
    created_at: datetime
    start_at: datetime
    end_at: datetime
    data: List[TripDataPoint]

    user: UserSchema
    nakamal: NakamalSchema


class TripSchemaOut(TripSchema):
    pass

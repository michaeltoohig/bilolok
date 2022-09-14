import uuid
from datetime import datetime
from typing import Optional

from pydantic import AnyHttpUrl

from app.schemas.base import BaseSchema
from app.schemas.nakamal import NakamalSchema


class CheckinSchemaBase(BaseSchema):
    private: Optional[bool] = False
    message: Optional[str] = None


# class CheckinUpdate(CheckinSchemaBase):
#     pass


class CheckinSchemaIn(CheckinSchemaBase):
    lat: Optional[float] = None
    lng: Optional[float] = None
    nakamal_id: uuid.UUID


# HACK see main `UserSchema` for explanation
class UserSchema(BaseSchema):
    id: uuid.UUID
    avatar: Optional[AnyHttpUrl] = None


class CheckinSchema(CheckinSchemaBase):
    id: uuid.UUID
    created_at: datetime
    user_id: uuid.UUID
    nakamal_id: uuid.UUID
    user: UserSchema
    nakamal: NakamalSchema


class CheckinSchemaOut(CheckinSchema):
    pass

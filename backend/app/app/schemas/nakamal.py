import uuid
from typing import List, Optional

from .base import BaseSchema


#
# Nakamal Resource
#


class NakamalResourceSchemaBase(BaseSchema):
    name: Optional[str] = None


class NakamalResourceSchemaIn(NakamalResourceSchemaBase):
    name: str


class NakamalResourceSchema(NakamalResourceSchemaBase):
    id: uuid.UUID
    name: str


class NakamalResourceSchemaOut(NakamalResourceSchema):
    pass


#
# Nakamal
#


class NakamalSchemaBase(BaseSchema):
    name: Optional[str] = None
    aliases: Optional[List[str]] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    owner: Optional[str] = None
    phone: Optional[str] = None
    light: Optional[str] = None
    windows: Optional[int] = None


class NakamalSchemaUpdate(NakamalSchemaBase):
    pass


class NakamalSchemaIn(NakamalSchemaBase):
    name: str
    light: str
    windows: int
    lat: float
    lng: float


class NakamalSchema(NakamalSchemaBase):
    id: uuid.UUID
    resources: List[NakamalResourceSchema]


class NakamalSchemaOut(NakamalSchema):
    pass

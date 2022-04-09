import uuid
from typing import List, Optional

from app.models.nakamal import Province

from .base import BaseSchema

#
# Nakamal Kava Source
#


class NakamalKavaSourceSchemaBase(BaseSchema):
    island: Optional[str] = None
    province: Optional[Province] = None


class NakamalKavaSourceSchemaIn(NakamalKavaSourceSchemaBase):
    province: Province


class NakamalKavaSourceSchema(NakamalKavaSourceSchemaBase):
    id: uuid.UUID
    province: Province


class NakamalKavaSourceSchemaOut(NakamalKavaSourceSchema):
    pass


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
# NakamalArea
#


class NakamalAreaSchemaBase(BaseSchema):
    name: Optional[str] = None


class NakamalAreaSchemaIn(NakamalAreaSchemaBase):
    name: str


class NakamalAreaSchema(NakamalAreaSchemaBase):
    id: uuid.UUID
    name: str


class NakamalAreaSchemaOut(NakamalAreaSchema):
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
    area_id: Optional[uuid.UUID] = None
    kava_source_id: Optional[uuid.UUID] = None


class NakamalSchemaIn(NakamalSchemaBase):
    name: str
    light: str
    windows: int
    lat: float
    lng: float
    area_id: uuid.UUID
    kava_source_id: uuid.UUID


class NakamalSchema(NakamalSchemaBase):
    id: uuid.UUID
    kava_source: NakamalKavaSourceSchema
    resources: List[NakamalResourceSchema]
    area: NakamalAreaSchema


class NakamalSchemaOut(NakamalSchema):
    pass

import uuid
from typing import Optional

from .base import BaseSchema


class NakamalSchemaBase(BaseSchema):
    name: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    owner: Optional[str] = None
    phone: Optional[str] = None
    light: Optional[str] = None


# class NakamalSchemaUpdate(NakamalSchemaBase):
#     pass


class NakamalSchemaIn(NakamalSchemaBase):
    name: str
    lat: float
    lng: float
    

class NakamalSchema(NakamalSchemaBase):
    id: uuid.UUID


class NakamalSchemaOut(NakamalSchema):
    pass

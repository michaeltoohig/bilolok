from typing import Optional
import uuid

from app.schemas.nakamal import NakamalSchema, NakamalSchemaOut

from .base import BaseSchema


class ImageSchemaBase(BaseSchema):
    pass


# class ImageSchemaUpdate(ImageSchemaBase):
#     pass


class ImageSchemaIn(ImageSchemaBase):
    file_id: str
    filename: str
    filetype: str
    user_id: uuid.UUID
    nakamal_id: uuid.UUID


class ImageSchema(ImageSchemaBase):
    id: uuid.UUID
    file_id: str
    filename: str
    user_id: uuid.UUID  # TODO replace with public user schema
    nakamal: NakamalSchema
    src: str
    msrc: str
    thumbnail: str


class ImageSchemaOut(ImageSchema):
    pass
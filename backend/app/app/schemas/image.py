from typing import Optional
import uuid

from .base import BaseSchema
from .nakamal import NakamalSchema, NakamalSchemaOut


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

    src: str
    msrc: str
    thumbnail: str
    
    user_id: uuid.UUID  # TODO replace with public user schema
    nakamal: NakamalSchema


class ImageSchemaOut(ImageSchema):
    pass
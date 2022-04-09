import uuid
from datetime import datetime

from .base import BaseSchema
from .nakamal import NakamalSchema
from .user import UserSchema


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
    created_at: datetime
    file_id: str
    filename: str

    src: str
    msrc: str
    thumbnail: str

    user: UserSchema
    nakamal: NakamalSchema


class ImageSchemaOut(ImageSchema):
    pass

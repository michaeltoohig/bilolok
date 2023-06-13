import uuid
from typing import Optional
from datetime import datetime
from pathlib import Path

from models.video import VideoProcessingStatus

from .base import BaseSchema
from .nakamal import NakamalSchema
from .user import UserSchema


class VideoSchemaBase(BaseSchema):
    pass


class VideoSchemaUpdate(VideoSchemaBase):
    status: VideoProcessingStatus


class VideoSchemaIn(VideoSchemaBase):
    file_id: str
    filename: str
    filetype: str
    status: VideoProcessingStatus = VideoProcessingStatus.PENDING
    user_id: uuid.UUID
    nakamal_id: Optional[uuid.UUID] = None


class VideoSchema(VideoSchemaBase):
    id: uuid.UUID
    created_at: datetime
    file_id: str
    filename: str
    filetype: str
    status: VideoProcessingStatus

    src: str
    cover: str
    social_thumbnail: str

    user: UserSchema
    nakamal: Optional[NakamalSchema] = None


class VideoSchemaOut(VideoSchema):
    pass

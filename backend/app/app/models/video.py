from enum import Enum

from pathlib import Path
from uuid import UUID

from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import Column, ForeignKey, String, Enum as SQLAEnum
from sqlalchemy.orm import relationship

from app.core.config import settings
from app.db.base_class import Base
from app.db.mixins import TimeMixin


class VideoProcessingStatus(Enum):
    PENDING = "PENDING"
    PROGRESS = "PROGRESS"
    COMPLETE = "COMPLETE"
    ERROR = "ERROR"


class Video(Base, TimeMixin):
    """SQLAlchemy videos table definition."""

    __tablename__ = "video"

    file_id = Column(String, unique=True, nullable=False)
    filename = Column(String)
    filetype = Column(String)
    # Processing
    status = Column(SQLAEnum(VideoProcessingStatus), nullable=False, default=VideoProcessingStatus.PENDING)
    # Relationships
    user_id = Column(GUID, ForeignKey("user.id"), nullable=False)
    user = relationship("User", lazy="joined")
    nakamal_id = Column(GUID, ForeignKey("nakamal.id"))
    nakamal = relationship("Nakamal", lazy="joined")

    @staticmethod
    def build_filepath(user_id: UUID, file_id: str, filename: str):
        VIDEO_PATH_FMT = "videos/{subdir}/{u_id}/{f_id}/{filename}"
        return Path(
            VIDEO_PATH_FMT.format(
                subdir=str(user_id)[:2],
                u_id=str(user_id),
                f_id=file_id,
                filename=filename,
            )
        )

    # @staticmethod
    # def build_full_filepath(filepath: Path):
    #     """Full path to file."""
    #     return Path(settings.DATA_LOCAL_DIR) / filepath


    # @property
    # def original_filepath(self, filename: str = None):
    #     """Relative path to file."""
    #     filename = "original/{f_id}{ext}".format(f_id=self.file_id, ext=Path(self.filename).suffix)
    #     return self.build_filepath(
    #         user_id=self.user_id,
    #         file_id=self.file_id,
    #         filename=filename,
    #     )

    # @property
    # def video_filepath(self):
    #     filename = "{f_id}.webm".format(self.file_id)
    #     return self.build_filepath(
    #         user_id=self.user_id,
    #         file_id=self.file_id,
    #         filename=filename,
    #     )

    # @property
    # def cover_filepath(self):
    #     filename = "{f_id}.jpg".format(self.file_id)
    #     return self.build_filepath(
    #         user_id=self.user_id,
    #         file_id=self.file_id,
    #         filename=filename,
    #     )

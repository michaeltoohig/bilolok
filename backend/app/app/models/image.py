from typing import Any, Dict, Optional
from pathlib import Path

import ormar
from pydantic import UUID4

from app.core.config import settings
from app.db.mixins import TimeMixin
from app.db.base_class import BaseMeta
from app.models.nakamal import Nakamal
from app.models.user import User

class Image(ormar.Model, TimeMixin):
    class Meta(BaseMeta):
        tablename = "image"
    
    id: UUID4 = ormar.UUID(primary_key=True, uuid_format="string")
    file_id: str = ormar.Text(unique=True, nullable=False)
    filename: str = ormar.Text()
    filetype: str = ormar.Text()
    # Relationships
    user: Optional[Dict[str, Any]] = ormar.ForeignKey(User)
    nakamal: Optional[Dict[str, Any]] = ormar.ForeignKey(Nakamal)
    # user_id = ormar.UUID(ForeignKey("user.id"), nullable=False)
    # nakamal_id = ormar.UUID(ForeignKey("nakamal.id"), nullable=False)

    # @staticmethod
    # def build_filepath(nakamal_id: str, file_id: str, filename: str):
    #     IMAGE_PATH_FMT = "nakamals/{subdir}/{n_id}/{f_id}{ext}"
    #     return Path(IMAGE_PATH_FMT.format(
    #         subdir=str(nakamal_id)[:2],
    #         n_id=str(nakamal_id),
    #         f_id=file_id,
    #         ext=Path(filename).suffix,
    #     ))

    # @property
    # def filepath(self):
    #     """Relative path to file."""
    #     return self.build_filepath(
    #         nakamal_id=self.nakamal_id,
    #         file_id=self.file_id,
    #         filename=self.filename,
    #     )

    # @property
    # def full_filepath(self):
    #     """Full path to file."""
    #     return Path(settings.IMAGES_LOCAL_DIR) / self.filepath

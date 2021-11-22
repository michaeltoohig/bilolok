from typing import Any, Dict, List, Optional
from pathlib import Path
import uuid

import ormar
from pydantic import AnyHttpUrl

from app.core.config import settings
from app.db.mixins import TimeMixin
from app.db.base_class import BaseMeta
# from app.models.nakamal import Nakamal
# from app.models.user import User


# class Image(ormar.Model, TimeMixin):
#     class Meta(BaseMeta):
#         tablename = "image"
    
#     id: uuid.UUID = ormar.UUID(primary_key=True, default=uuid.uuid4, uuid_format="string")
#     file_id: str = ormar.Text(unique=True, nullable=False)
#     filename: str = ormar.Text()
#     filetype: str = ormar.Text()
#     # Relationships
#     user: Optional[Dict[str, Any]] = ormar.ForeignKey(User, name="user_id")
#     nakamal: Optional[Dict[str, Any]] = ormar.ForeignKey(Nakamal, name="nakamal_id")
#     # Pydantic fields
#     src: Optional[AnyHttpUrl] = None
#     msrc: Optional[AnyHttpUrl] = None
#     thumbnail: Optional[AnyHttpUrl] = None

#     @staticmethod
#     def build_filepath(nakamal_id: str, file_id: str, filename: str):
#         IMAGE_PATH_FMT = "nakamals/{subdir}/{n_id}/{f_id}{ext}"
#         return Path(IMAGE_PATH_FMT.format(
#             subdir=str(nakamal_id)[:2],
#             n_id=str(nakamal_id),
#             f_id=file_id,
#             ext=Path(filename).suffix,
#         ))

#     @property
#     def filepath(self):
#         """Relative path to file."""
#         return self.build_filepath(
#             nakamal_id=self.nakamal_id,
#             file_id=self.file_id,
#             filename=self.filename,
#         )

#     @property
#     def full_filepath(self):
#         """Full path to file."""
#         return Path(settings.IMAGES_LOCAL_DIR) / self.filepath

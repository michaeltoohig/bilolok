from typing import Any, Dict, Optional
from pathlib import Path
import uuid

import ormar
from ormar import property_field
from fastapi_users.db import OrmarBaseUserModel
from pydantic import AnyHttpUrl
from pydantic.typing import ForwardRef

from app.core.config import settings
from app.core.image import img_crypto_url
from app.db.base_class import BaseMeta
from app.db.session import metadata, database
from app.db.mixins import TimeMixin


class User(OrmarBaseUserModel):
    class Meta(BaseMeta):
        tablename = "user"


ImageRef = ForwardRef("Image")


class Nakamal(ormar.Model):
    class Meta:
        tablename = "nakamal"
        metadata = metadata
        database = database

    id: uuid.UUID = ormar.UUID(primary_key=True, default=uuid.uuid4, uuid_format="string")
    name: str = ormar.Text(nullable=False)
    lat: float = ormar.Float(nullable=False)
    lng: float = ormar.Float(nullable=False)
    light: str = ormar.Text()
    owner: str = ormar.Text()
    phone: str = ormar.Text()

    image: Optional[ImageRef] = None


class Image(ormar.Model, TimeMixin):
    class Meta(BaseMeta):
        tablename = "image"
    
    id: uuid.UUID = ormar.UUID(primary_key=True, default=uuid.uuid4, uuid_format="string")
    file_id: str = ormar.Text(unique=True, nullable=False)
    filename: str = ormar.Text()
    filetype: str = ormar.Text()
    # Relationships
    user: Optional[Dict[str, Any]] = ormar.ForeignKey(User, name="user_id")
    nakamal: Optional[Dict[str, Any]] = ormar.ForeignKey(Nakamal, name="nakamal_id")
    
    # Pydantic fields
    # src: Optional[AnyHttpUrl] = None
    # msrc: Optional[AnyHttpUrl] = None
    # thumbnail: Optional[AnyHttpUrl] = None

    @property_field
    def src(self):
        return self.make_src(height=1080, width=1920, full_fit_in=True)
        
    @property_field
    def msrc(self):
        return self.make_src(height=32, width=32, full_fit_in=True)
        
    @property_field
    def thumbnail(self):
        return self.make_src(height=200, width=200)

    def make_src(self, width: int, height: int, **kwargs) -> str:
        uri = img_crypto_url.generate(
            width=width,
            height=height,
            smart=True,
            image_url=str(Image.build_filepath(self.nakamal.id, self.file_id, self.filename)),
            **kwargs,
        )
        return "{}{}".format(settings.THUMBOR_SERVER, uri)

    @staticmethod
    def build_filepath(nakamal_id: str, file_id: str, filename: str):
        IMAGE_PATH_FMT = "nakamals/{subdir}/{n_id}/{f_id}{ext}"
        return Path(IMAGE_PATH_FMT.format(
            subdir=str(nakamal_id)[:2],
            n_id=str(nakamal_id),
            f_id=file_id,
            ext=Path(filename).suffix,
        ))

    @property
    def filepath(self):
        """Relative path to file."""
        return self.build_filepath(
            nakamal_id=self.nakamal_id,
            file_id=self.file_id,
            filename=self.filename,
        )

    @property
    def full_filepath(self):
        """Full path to file."""
        return Path(settings.IMAGES_LOCAL_DIR) / self.filepath


Nakamal.update_forward_refs()

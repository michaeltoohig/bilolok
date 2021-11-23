from typing import Any, Dict, Optional, Union
from pathlib import Path
import uuid

from fastapi_users.db import OrmarBaseUserModel
import ormar
from ormar import property_field
import pydantic

from app.core.config import settings
from app.core.image import img_crypto_url
from app.db.base_class import BaseMeta
from app.db.session import metadata, database
from app.db.mixins import TimeMixin


class User(OrmarBaseUserModel):
    class Meta(BaseMeta):
        tablename = "user"


class Nakamal(ormar.Model):
    class Meta(BaseMeta):
        tablename = "nakamal"

    id: uuid.UUID = ormar.UUID(primary_key=True, default=uuid.uuid4, uuid_format="string")
    name: str = ormar.Text(nullable=False)
    lat: float = ormar.Float(nullable=False)
    lng: float = ormar.Float(nullable=False)
    light: str = ormar.Text()
    owner: str = ormar.Text()
    phone: str = ormar.Text()


class Image(ormar.Model, TimeMixin):
    class Meta(BaseMeta):
        tablename = "image"
        orders_by = ["-created_at"]
    
    id: uuid.UUID = ormar.UUID(primary_key=True, default=uuid.uuid4, uuid_format="string")
    file_id: str = ormar.Text(unique=True, nullable=False)
    filename: str = ormar.Text()
    filetype: str = ormar.Text()
    # Relationships
    user: Union[User, Dict[str, Any]] = ormar.ForeignKey(User, nullable=False, name="user_id")
    nakamal: Union[Nakamal, Dict[str, Any]] = ormar.ForeignKey(
        Nakamal,
        nullable=False,
        name="nakamal_id",
        orders_by=["name"],
        related_orders_by=["-created_at"],
    )
    
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


class Checkin(ormar.Model, TimeMixin):
    class Meta(BaseMeta):
        tablename = "checkin"
        orders_by = ["-created_at"]

    id: uuid.UUID = ormar.UUID(primary_key=True, default=uuid.uuid4, uuid_format="string")
    private: bool = ormar.Boolean(nullable=False, default=False)
    message: str = ormar.Text(nullable=True)
    lat: float = ormar.Float(nullable=True)
    lng: float = ormar.Float(nullable=True)
    # Relationships
    user: Union[User, Dict[str, Any]] = ormar.ForeignKey(
        User,
        nullable=False,
        name="user_id",
        orders_by=["email"],
        related_orders_by=["-created_at"],
    )
    nakamal: Union[Nakamal, Dict[str, Any]] = ormar.ForeignKey(Nakamal, nullable=False, name="nakamal_id")


class CheckinCreate(pydantic.BaseModel):
    nakamal: uuid.UUID
    private: bool = False
    message: str = None
    lat: float = None
    lng: float = None

    class Config:
        orm_mode = True

# CheckinCreate = Checkin.get_pydantic(
#     include={
#         "nakamal": {"id"},
#     },
#     exclude={
#         "created_at": ...,
#         "updated_at": ...,
#         "user": ...,
#         "nakamal": ...,
#     }
# )

from pathlib import Path
from uuid import UUID

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, String

from app.core.config import settings
from app.core.image import img_crypto_url
from app.db.base_class import Base

# from .fastapi_users_db_sqlalchemy_asyncpg import SQLAlchemyBaseUserTable



class User(Base, SQLAlchemyBaseUserTable):
    avatar_filename = Column(String)

    @property
    def avatar(self):
        uri = img_crypto_url.generate(
            width=100,
            height=100,
            smart=True,
            image_url=str(User.build_avatar_filepath(self.id, self.avatar_filename)),
        )
        return "{}{}".format(settings.THUMBOR_SERVER, uri)

    @staticmethod
    def build_avatar_filepath(user_id: UUID, filename: str = None):
        if filename is None:
            filename = "default.png"
        IMAGE_PATH_FMT = "users/{subdir}/{u_id}/{filename}"
        return Path(
            IMAGE_PATH_FMT.format(
                subdir=str(user_id)[:2],
                u_id=str(user_id),
                filename=filename,
            )
        )

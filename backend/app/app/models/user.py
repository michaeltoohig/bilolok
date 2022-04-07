from pathlib import Path
from uuid import UUID

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
# from .fastapi_users_db_sqlalchemy_asyncpg import SQLAlchemyBaseUserTable

from app.core.config import settings
from app.core.image import img_crypto_url
from app.db.base_class import Base


class User(Base, SQLAlchemyBaseUserTable):

    @property
    def avatar(self):
        uri = img_crypto_url.generate(
            width=100,
            height=100,
            smart=True,
            image_url=str(User.build_avatar_filepath(self.id)),
        )
        return "{}{}".format(settings.THUMBOR_SERVER, uri)
    
    @staticmethod
    def build_avatar_filepath(user_id: UUID):
        IMAGE_PATH_FMT = "users/{subdir}/{u_id}/default.png"
        return Path(IMAGE_PATH_FMT.format(
            subdir=str(user_id)[:2],
            u_id=str(user_id),
        ))

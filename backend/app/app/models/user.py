from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core.config import settings
from app.db.base_class import Base


class User(Base, SQLAlchemyBaseUserTable):
    pass

    # In future can add `name` that will display
    # in feed or whatever. for now just have messages
    # like `1 person likes` or `2 people are at...`

UserTable = User.__table__

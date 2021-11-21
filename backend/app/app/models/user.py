from fastapi_users.db import OrmarBaseUserModel

from app.db.base_class import BaseMeta


class User(OrmarBaseUserModel):
    class Meta(BaseMeta):
        tablename = "user"

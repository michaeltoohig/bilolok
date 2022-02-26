from typing import Type
from uuid import UUID

from sqlalchemy import desc

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserSchema


class CRUDUser(CRUDBase[User, UserCreate, UserSchema]):    
    @property
    def _in_schema(self) -> Type[UserCreate]:
        return UserCreate

    @property
    def _schema(self) -> Type[UserSchema]:
        return UserSchema

    @property
    def _table(self) -> Type[User]:
        return User

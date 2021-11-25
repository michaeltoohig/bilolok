from typing import Any, List, Dict, Optional, Type
from pathlib import Path

from fastapi_crudrouter.core.databases import pydantify_record
from sqlalchemy import desc

from app.core.config import settings
from app.core.image import img_crypto_url
from app.crud.base import CRUDBase
from app.db.session import database
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
    
from typing import Optional
import uuid

from fastapi_users import models
from app.schemas.base import BaseSchema
from pydantic import AnyHttpUrl


# TODO update schema class names to match other schemas naming convention


class User(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(models.BaseUserUpdate):
    avatar_filename: Optional[str] = None


class UserDB(User, models.BaseUserDB):
    pass
    # avatar: Optional[AnyHttpUrl] = None


# Additional schema for public facing API
class UserSchema(BaseSchema):
    id: uuid.UUID
    avatar: Optional[AnyHttpUrl] = None
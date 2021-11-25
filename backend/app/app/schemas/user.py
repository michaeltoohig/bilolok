import uuid
from typing import List, Optional, TypeVar

from fastapi_users import models
from pydantic import BaseModel, EmailStr, Field


# TODO update schema class names to match other schemas naming convention


class User(models.BaseUser):
    pass


class UserCreate(models.BaseUserCreate):
    pass


class UserUpdate(models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass


# Additional schema for public facing API
class UserSchema(models.BaseUser):
    id: uuid.UUID

    class Config:
        orm_mode = True
import uuid
from typing import ForwardRef, Optional

from fastapi_users import models
from pydantic import AnyHttpUrl

from app.schemas.base import BaseSchema

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


# NOTE the `UserSchema` is copied into a few other schema files 
#  due to limitation of Pydantic. We need the `UserSchema` for
#  a few different schemas but there were circular imports and
#  `ForwardRef` or other solutions do not work for more than
#  a single two-way binding. 


CheckinSchema = ForwardRef("CheckinSchema")


class UserSchemaDetails(UserSchema):
    latest_checkin: Optional[CheckinSchema]


from app.schemas.checkin import CheckinSchema
UserSchemaDetails.update_forward_refs()

from fileinput import filename
import uuid
from typing import Any, List, Optional

from models.nakamal import Province
from pydantic import AnyHttpUrl

from .base import BaseSchema


#
# Nakamal Kava Source
#


class NakamalKavaSourceSchemaBase(BaseSchema):
    island: Optional[str] = None
    province: Optional[Province] = None


class NakamalKavaSourceSchemaIn(NakamalKavaSourceSchemaBase):
    province: Province


class NakamalKavaSourceSchema(NakamalKavaSourceSchemaBase):
    id: uuid.UUID
    province: Province


class NakamalKavaSourceSchemaOut(NakamalKavaSourceSchema):
    pass


#
# Nakamal Resource
#


class NakamalResourceSchemaBase(BaseSchema):
    name: Optional[str] = None


class NakamalResourceSchemaIn(NakamalResourceSchemaBase):
    name: str


class NakamalResourceSchema(NakamalResourceSchemaBase):
    id: uuid.UUID
    name: str


class NakamalResourceSchemaOut(NakamalResourceSchema):
    pass


#
# NakamalArea
#


class NakamalAreaSchemaBase(BaseSchema):
    name: Optional[str] = None


class NakamalAreaSchemaIn(NakamalAreaSchemaBase):
    name: str


class NakamalAreaSchema(NakamalAreaSchemaBase):
    id: uuid.UUID
    name: str


class NakamalAreaSchemaOut(NakamalAreaSchema):
    pass


#
# Nakamal
#


class NakamalSchemaBase(BaseSchema):
    name: Optional[str] = None
    aliases: Optional[List[str]] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    owner: Optional[str] = None
    phone: Optional[str] = None
    light: Optional[str] = None
    windows: Optional[int] = None


class NakamalSchemaUpdate(NakamalSchemaBase):
    area_id: Optional[uuid.UUID] = None
    kava_source_id: Optional[uuid.UUID] = None


class NakamalSchemaIn(NakamalSchemaBase):
    name: str
    light: str
    windows: int
    lat: float
    lng: float
    area_id: uuid.UUID
    kava_source_id: uuid.UUID


# TODO return ID only allow frontend to handle fetching user info
# HACK see `UserSchema` in schemas/user.py for explanation
class UserSchema(BaseSchema):
    id: uuid.UUID
    avatar: Optional[AnyHttpUrl] = None


# # HACK see `UserSchema` in schemas/user.py for explanation
# class ImageSchema(BaseSchema):
#     id: uuid.UUID
#     src: str
#     msrc: str
#     thumbnail: str
    
#     # to `make_img_src` in CRUDImage we need `.nakamal.id` which means 
#     # we would load the image for the nakaml then load the nakamal as a sub-item
#     # of the image again making a loop.
#     # This idea of loading the profile picture and its info at the same time as
#     # the nakamal is not going to work and is better served as either returning
#     # the image ID only and allow the client to fetch the image if it is not in
#     # cache already OR fetch the profile and add it to the response but that requires
#     # modifying a lot of code to ensure the profile picture is included in every
#     # nakamal request.
#     # The third option to accept that the way I build an `ImageSchema` to include the
#     # src/thumbnail is bad now and needs to be refactored to handle this new usecase. 
#     file_id: str
#     filename: str
#     filetype: str
#     user_id: uuid.UUID
#     nakamal_id: uuid.UUID


class NakamalSchema(NakamalSchemaBase):
    id: uuid.UUID
    chief: Optional[UserSchema] = None
    # profile: Optional[ImageSchema] = None
    profile_id: Optional[uuid.UUID] = None
    kava_source: NakamalKavaSourceSchema
    resources: List[NakamalResourceSchema]
    area: NakamalAreaSchema


class NakamalSchemaOut(NakamalSchema):
    pass

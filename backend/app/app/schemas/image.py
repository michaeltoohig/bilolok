import uuid
from typing import Optional
from pydantic import BaseModel, UUID4, validator
from pydantic.networks import HttpUrl


class ImageBase(BaseModel):
    pass


class ImageUpdate(ImageBase):
    pass


class ImageCreate(ImageBase):
    id: Optional[UUID4] = None
    file_id: str
    filename: str
    filetype: str
    user_id: UUID4
    nakamal_id: UUID4

    @validator("id", pre=True, always=True)
    def default_id(cls, v):
        return v or uuid.uuid4()


class ImageDB(ImageBase):
    id: UUID4
    file_id: str
    user_id: UUID4
    nakamal_id: UUID4
    src: str
    thumbnail: str

    class Config:
        orm_mode = True

import uuid
from typing import Optional
from app.schemas.image import ImageDB
from pydantic import BaseModel, UUID4, validator


class NakamalBase(BaseModel):
    name: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    owner: Optional[str] = None
    phone: Optional[str] = None
    light: Optional[str] = None


class NakamalUpdate(NakamalBase):
    pass


class NakamalCreate(NakamalBase):
    id: Optional[UUID4] = None
    name: str
    lat: float
    lng: float
    
    @validator("id", pre=True, always=True)
    def default_id(cls, v):
        return v or uuid.uuid4()


class NakamalDB(NakamalBase):
    id: UUID4
    image: Optional[ImageDB] = None

    class Config:
        orm_mode = True


# class NakamalMessageCreate(BaseModel):
#     body: str
#     nakamal_id: int


# class NakamalMessage(NakamalCreate):
#     id: int
#     created_at: datetime
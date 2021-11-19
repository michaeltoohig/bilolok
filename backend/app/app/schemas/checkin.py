import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, UUID4, validator


class CheckinBase(BaseModel):
    private: Optional[bool] = False
    message: Optional[str] = None


class CheckinUpdate(CheckinBase):
    pass


class CheckinCreate(CheckinBase):
    id: Optional[UUID4] = None
    user_id: UUID4
    nakamal_id: UUID4
    lat: Optional[float] = None
    lng: Optional[float] = None
    
    @validator("id", pre=True, always=True)
    def default_id(cls, v):
        return v or uuid.uuid4()


class CheckinDB(CheckinBase):
    id: UUID4
    user_id: UUID4
    nakamal_id: UUID4
    created_at: datetime

    class Config:
        orm_mode = True

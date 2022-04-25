from enum import Enum
from pathlib import Path
from typing import Any, List, Optional
from app.crud.video import CRUDVideo
from app.schemas.video import VideoSchemaIn

import jwt
from fastapi import Body, Depends, Header, HTTPException, status, APIRouter
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from fastapi_users.jwt import JWT_ALGORITHM
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.api.deps.db import get_db
from app.api.deps.video import get_video_or_404
from app.api.deps.user import current_superuser
from app.core.config import settings
from app.core.users import UserManager, get_jwt_strategy, get_user_manager
from app.crud.video import CRUDVideo
from app.crud.nakamal import CRUDNakamal
from app.crud.user import CRUDUser
from app.models.video import Video
from app.models.user import User
from app.schemas.video import VideoSchema, VideoSchemaIn, VideoSchemaOut

router = APIRouter(prefix="/videos")


@router.get(
    "",
    response_model=List[VideoSchemaOut],
)
async def get_all(
    db: AsyncSession = Depends(get_db),
    *,
    skip: Optional[int] = 0,
    limit: Optional[int] = 100,
) -> List[VideoSchemaOut]:
    crud_video = CRUDVideo(db)
    items = await crud_video.get_multi(skip=skip, limit=limit)
    return [VideoSchemaOut(**item.dict()) for item in items]


@router.get(
    "/{item_id:uuid}",
    response_model=VideoSchemaOut,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "detail": "Video not found.",
        },
    },
)
async def get_one(
    db: AsyncSession = Depends(get_db),
    *,
    item: VideoSchema = Depends(get_video_or_404),
) -> VideoSchemaOut:
    return VideoSchemaOut(**item.dict())


@router.delete(
    "/{item_id:uuid}",
    response_model=VideoSchemaOut,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "detail": "Video not found.",
        },
    },
)
async def delete_one(
    db: AsyncSession = Depends(get_db),
    superuser: User = Depends(current_superuser),
    *,
    item: VideoSchema = Depends(get_video_or_404)
) -> VideoSchemaOut:
    crud_video = CRUDVideo(db)
    item = await crud_video.delete(item.id)
    return VideoSchemaOut(**item.dict())
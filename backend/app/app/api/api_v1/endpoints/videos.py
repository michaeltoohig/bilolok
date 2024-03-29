from enum import Enum
from pathlib import Path
from typing import Any, List, Optional
from crud.video import CRUDVideo
from schemas.video import VideoSchemaIn

import jwt
from fastapi import Body, Depends, Header, HTTPException, status, APIRouter, Query
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from fastapi_users.jwt import JWT_ALGORITHM
from sqlalchemy.ext.asyncio.session import AsyncSession

from api.deps.db import get_db
from api.deps.video import get_video_or_404
from api.deps.user import current_active_verified_user, current_superuser
from core.config import settings
from core.users import UserManager, get_jwt_strategy, get_user_manager
from crud.video import CRUDVideo
from crud.nakamal import CRUDNakamal
from crud.user import CRUDUser
from models.video import Video
from models.user import User
from schemas.video import VideoSchema, VideoSchemaIn, VideoSchemaOut

router = APIRouter(prefix="/videos")


@router.get(
    "",
    response_model=List[VideoSchemaOut],
)
async def get_all(
    db: AsyncSession = Depends(get_db),
    *,
    recent: bool = Query(False),
    skip: Optional[int] = 0,
    limit: Optional[int] = 100,
) -> List[VideoSchemaOut]:
    crud_video = CRUDVideo(db)
    if recent:
        items = await crud_video.get_recent()
    else:
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
    item: VideoSchema = Depends(get_video_or_404),
) -> VideoSchemaOut:
    """A video"""
    return VideoSchemaOut(**item.dict())


@router.delete(
    "/{item_id:uuid}",
    response_model=VideoSchemaOut,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "detail": "User does not have permission to delete this video."
        },
        status.HTTP_404_NOT_FOUND: {
            "detail": "Video not found.",
        },
    },
)
async def delete_one(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_verified_user),
    *,
    item: VideoSchema = Depends(get_video_or_404)
) -> VideoSchemaOut:
    """Delete a video"""
    if not user.is_superuser:
        if user.id != item.user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    crud_video = CRUDVideo(db)
    item = await crud_video.delete(item.id)
    return VideoSchemaOut(**item.dict())

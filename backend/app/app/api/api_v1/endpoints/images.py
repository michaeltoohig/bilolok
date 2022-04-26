from enum import Enum
from pathlib import Path
from typing import Any, List, Optional
from app.crud.video import CRUDVideo
from app.schemas.video import VideoSchemaIn

import jwt
from fastapi import Body, Depends, Header, HTTPException, status, APIRouter, Query
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from fastapi_users.jwt import JWT_ALGORITHM
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.api.deps.db import get_db
from app.api.deps.image import get_image_or_404
from app.api.deps.user import current_active_verified_user, current_superuser
from app.core.config import settings
from app.core.users import UserManager, get_jwt_strategy, get_user_manager
from app.crud.image import CRUDImage
from app.crud.nakamal import CRUDNakamal
from app.crud.user import CRUDUser
from app.models.image import Image
from app.models.user import User
from app.schemas.image import ImageSchema, ImageSchemaIn, ImageSchemaOut

# # TODO remove this CRUDRouter as we are no longer even using it due to special schema handling
# router = SQLAlchemyCRUDRouter(
#     prefix="images",
#     tags=["images"],
#     schema=ImageSchema,
#     create_schema=ImageSchemaIn,
#     db_model=Image,
#     db=get_db,
#     get_one_route=False,
#     get_all_route=False,
#     delete_all_route=False,
#     update_route=False,
#     create_route=False,
#     delete_one_route=False,
# )

router = APIRouter(prefix="/images")


@router.get(
    "",
    response_model=List[ImageSchemaOut],
)
async def get_all(
    db: AsyncSession = Depends(get_db),
    *,
    recent: bool = Query(False),
    skip: Optional[int] = 0,
    limit: Optional[int] = 100,
) -> List[ImageSchemaOut]:
    crud_image = CRUDImage(db)
    if recent:
        items = await crud_image.get_recent()
    else:
        items = await crud_image.get_multi(skip=skip, limit=limit)
    return [ImageSchemaOut(**item.dict()) for item in items]


@router.get(
    "/{item_id:uuid}",
    response_model=ImageSchemaOut,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "detail": "Image not found.",
        },
    },
)
async def get_one(
    db: AsyncSession = Depends(get_db),
    *,
    item: ImageSchema = Depends(get_image_or_404),
) -> ImageSchemaOut:
    return ImageSchemaOut(**item.dict())


@router.delete(
    "/{item_id:uuid}",
    response_model=ImageSchemaOut,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "detail": "User does not have permission to delete this image."
        },
        status.HTTP_404_NOT_FOUND: {
            "detail": "Image not found.",
        },
    },
)
async def delete_one(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_verified_user),
    *,
    item: ImageSchema = Depends(get_image_or_404)
) -> ImageSchemaOut:
    """Delete an image"""
    if not user.is_superuser:
        if user.id != item.user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    crud_image = CRUDImage(db)
    item = await crud_image.delete(item.id)
    return ImageSchemaOut(**item.dict())

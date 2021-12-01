from typing import Any, List
from app.crud.image import CRUDImage
from app.schemas.checkin import CheckinSchemaOut
from app.schemas.image import ImageSchemaOut

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.checkin import CRUDCheckin
from app.crud.user import CRUDUser
from app.api.deps.db import get_db
from app.api.deps.user import current_superuser
from app.core.users import fastapi_users
from app.schemas.user import UserSchema

router = fastapi_users.get_users_router()


@router.get("", response_model=List[UserSchema])
async def get_all(
    db: AsyncSession = Depends(get_db)
) -> Any:
    crud_user = CRUDUser(db)
    items = await crud_user.get_multi()
    return [UserSchema(**item.dict()) for item in items]


@router.get("/{item_id}/images", response_model=List[ImageSchemaOut])
async def get_all_images(
    db: AsyncSession = Depends(get_db),
    *,
    item_id: str
) -> Any:
    # TODO user dependency
    crud_user = CRUDUser(db)
    item = await crud_user.get_by_id(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    crud_image = CRUDImage(db)
    images = await crud_image.get_multi_by_user(item.id)
    return [ImageSchemaOut(**image.dict()) for image in images]


@router.get("/{item_id}/checkins", response_model=List[CheckinSchemaOut])
async def get_all_checkins(
    db: AsyncSession = Depends(get_db),
    *,
    item_id: str
) -> Any:
    # TODO user dependency
    crud_user = CRUDUser(db)
    item = await crud_user.get_by_id(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    crud_checkin = CRUDCheckin(db)
    checkins = await crud_checkin.get_multi_by_user(item.id)
    return [CheckinSchemaOut(**checkin.dict()) for checkin in checkins]

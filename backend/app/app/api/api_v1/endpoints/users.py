from typing import Any, List, Optional, Union

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.db import get_db
from app.api.deps.user import optional_current_superuser
from app.core.users import UserManager, fastapi_users, get_user_manager
from app.crud.checkin import CRUDCheckin
from app.crud.image import CRUDImage
from app.crud.user import CRUDUser
from app.models.user import User
from app.schemas.checkin import CheckinSchemaOut
from app.schemas.image import ImageSchemaOut
from app.schemas.user import UserDB, UserSchema, UserUpdate

router = fastapi_users.get_users_router()


@router.get("", response_model=Union[List[UserDB], List[UserSchema]])
async def get_all(
    db: AsyncSession = Depends(get_db),
    *,
    superuser: Optional[User] = Depends(optional_current_superuser),
    user_manager: UserManager = Depends(get_user_manager),
) -> Any:
    """
    Return a list of users. Super Users will see the complete user profile
    for administrative purposes, others will see the public user schema.
    """
    if superuser:
        items = await user_manager.get_multi()
        return [UserDB(**item.dict()) for item in items]
    else:
        crud_user = CRUDUser(db)
        items = await crud_user.get_multi()
        return [UserSchema(**item.dict()) for item in items]


@router.delete("/{item_id}/profile", response_model=UserSchema)
async def delete_profile(
    db: AsyncSession = Depends(get_db),
    *,
    item_id: str,
) -> Any:
    crud_user = CRUDUser(db)
    item = await crud_user.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    update_schema = UserUpdate(**item.dict())
    update_schema.avatar_filename = None
    item = await crud_user.update(item.id, update_schema=update_schema)
    return UserSchema(**item.dict())


@router.get("/{item_id}/images", response_model=List[ImageSchemaOut])
async def get_all_images(db: AsyncSession = Depends(get_db), *, item_id: str) -> Any:
    # TODO user dependency
    crud_user = CRUDUser(db)
    item = await crud_user.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    crud_image = CRUDImage(db)
    images = await crud_image.get_multi_by_user(item.id)
    return [ImageSchemaOut(**image.dict()) for image in images]


@router.get("/{item_id}/checkins", response_model=List[CheckinSchemaOut])
async def get_all_checkins(db: AsyncSession = Depends(get_db), *, item_id: str) -> Any:
    # TODO user dependency
    crud_user = CRUDUser(db)
    item = await crud_user.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    crud_checkin = CRUDCheckin(db)
    checkins = await crud_checkin.get_multi_by_user(item.id)
    return [CheckinSchemaOut(**checkin.dict()) for checkin in checkins]

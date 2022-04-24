from typing import Any, List, Optional, Union
from app.crud.video import CRUDVideo
from app.schemas.video import VideoSchemaOut

from pydantic import UUID4
from fastapi import Depends, HTTPException, Request, status, APIRouter, Query
from fastapi_users.manager import InvalidPasswordException, UserAlreadyExists, UserNotExists
from fastapi_users.router.common import ErrorCode, ErrorModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.db import get_db
from app.api.deps.user import current_active_user, current_superuser, optional_current_superuser
from app.core.users import UserManager, get_user_manager
from app.crud.checkin import CRUDCheckin
from app.crud.image import CRUDImage
from app.crud.user import CRUDUser
from app.crud.trip import CRUDTrip
from app.models.user import User
from app.schemas.checkin import CheckinSchemaOut
from app.schemas.image import ImageSchemaOut
from app.schemas.trip import TripSchemaOut
from app.schemas.user import UserDB, UserSchema, UserSchemaDetails, UserUpdate

# NOTE in this router we approximate the endpoints provided by the
# FastAPI-Users user_router. I made some changes to support returning
# user objects as either the public facing `UserSchema` or the administrative
# schema `UserDB`.

router = APIRouter()


@router.get(
    "/me",
    response_model=UserDB,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user.",
        },
    },
)
async def get_me(
    user = Depends(current_active_user),
) -> Any:
    return user


@router.patch(
    "/me",
    response_model=UserDB,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user.",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS: {
                            "summary": "A user with this email already exists.",
                            "value": {
                                "detail": ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS
                            },
                        },
                        ErrorCode.UPDATE_USER_INVALID_PASSWORD: {
                            "summary": "Password validation failed.",
                            "value": {
                                "detail": {
                                    "code": ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                                    "reason": "Password should be"
                                    "at least 3 characters",
                                }
                            },
                        },
                    }
                }
            },
        },
    },
)
async def update_me(
    request: Request,
    user_update: UserUpdate,
    user = Depends(current_active_user),
    user_manager: UserManager = Depends(get_user_manager),
) -> Any:
    try:
        return await user_manager.update(
            user_update, user, safe=True, request=request
        )
    except InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )
    except UserAlreadyExists:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS,
        )


@router.get("")  #, response_model=Union[List[UserDB], List[UserSchemaDetails], List[UserSchema]])
async def get_all(
    db: AsyncSession = Depends(get_db),
    *,
    include_details: bool = Query(None, alias="includeDetails"),
    auth: bool = Query(None),
    superuser: Optional[User] = Depends(optional_current_superuser),
    user_manager: UserManager = Depends(get_user_manager),
) -> Any:
    """
    Return a list of users. Super Users will see the complete user profile
    for administrative purposes, others will see the public user schema.
    """
    if superuser and auth:
        items = await user_manager.get_multi()
        return [UserDB(**item.dict()) for item in items]
    else:
        crud_user = CRUDUser(db)
        items = await crud_user.get_multi()
        if include_details:
            data = []
            crud_checkin = CRUDCheckin(db)
            for item in items:
                latest = await crud_checkin.get_last_by_user(item.id)
                details = UserSchemaDetails(
                    **item.dict(),
                    latest_checkin=latest,
                )
                data.append(details.dict(exclude={"latest_checkin": {"user": ...}}))
            return data
        else:
            return [UserSchema(**item.dict()) for item in items]


@router.get(
    "/{item_id:uuid}",
    response_model=Union[UserDB, UserSchema],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user.",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Not a superuser.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The user does not exist.",
        },
    },
)
async def get_user(
    db: AsyncSession = Depends(get_db),
    *,
    item_id: UUID4,
    auth: bool = Query(None),
    superuser: Optional[User] = Depends(optional_current_superuser),
    user_manager: UserManager = Depends(get_user_manager),
) -> Any:
    if superuser and auth:
        item = await user_manager.get(item_id)
        return UserDB(**item.dict())
    else:
        crud_user = CRUDUser(db)
        item = await crud_user.get_by_id(item_id)
        return UserSchema(**item.dict())


@router.patch(
    "/{item_id:uuid}",
    response_model=UserDB,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing token or inactive user.",
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Not a superuser.",
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "The user does not exist.",
        },
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorModel,
            "content": {
                "application/json": {
                    "examples": {
                        ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS: {
                            "summary": "A user with this email already exists.",
                            "value": {
                                "detail": ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS
                            },
                        },
                        ErrorCode.UPDATE_USER_INVALID_PASSWORD: {
                            "summary": "Password validation failed.",
                            "value": {
                                "detail": {
                                    "code": ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                                    "reason": "Password should be"
                                    "at least 3 characters",
                                }
                            },
                        },
                    }
                }
            },
        },
    },
)
async def update_user(
    item_id: UUID4,
    request: Request,
    user_update: UserUpdate,
    user_manager: UserManager = Depends(get_user_manager),
    superuser: User = Depends(current_superuser),
) -> Any:
    try:
        user = await user_manager.get(item_id)
    except UserNotExists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    try:
        return await user_manager.update(
            user_update, user, safe=False, request=request
        )
    except InvalidPasswordException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": ErrorCode.UPDATE_USER_INVALID_PASSWORD,
                "reason": e.reason,
            },
        )
    except UserAlreadyExists:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=ErrorCode.UPDATE_USER_EMAIL_ALREADY_EXISTS,
        )


@router.delete("/{item_id:uuid}/profile", response_model=UserSchema)
async def delete_profile_picture(
    db: AsyncSession = Depends(get_db),
    *,
    item_id: UUID4,
    user: User = Depends(current_active_user),
) -> Any:
    crud_user = CRUDUser(db)
    if user.id != item_id:
        if not user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="You may only delete your own profile picture."
            )
    item = await crud_user.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    update_schema = UserUpdate(**item.dict())
    update_schema.avatar_filename = None
    item = await crud_user.update(item.id, update_schema=update_schema)
    return UserSchema(**item.dict())


@router.get("/{item_id:uuid}/images", response_model=List[ImageSchemaOut])
async def get_all_images(db: AsyncSession = Depends(get_db), *, item_id: UUID4) -> Any:
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


@router.get("/{item_id:uuid}/checkins", response_model=List[CheckinSchemaOut])
async def get_all_checkins(db: AsyncSession = Depends(get_db), *, item_id: UUID4) -> Any:
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


@router.get("/{item_id:uuid}/trips", response_model=List[TripSchemaOut])
async def get_all_trips(db: AsyncSession = Depends(get_db), *, item_id: UUID4) -> Any:
    # TODO user dependency
    crud_user = CRUDUser(db)
    item = await crud_user.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    crud_trip = CRUDTrip(db)
    trips = await crud_trip.get_multi_by_user(item.id)
    return [TripSchemaOut(**trip.dict()) for trip in trips]


@router.get("/{item_id:uuid}/videos", response_model=List[VideoSchemaOut])
async def get_all_videos(db: AsyncSession = Depends(get_db), *, item_id: UUID4) -> Any:
    # TODO user dependency
    crud_user = CRUDUser(db)
    item = await crud_user.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    crud_video = CRUDVideo(db)
    videos = await crud_video.get_multi_by_user(item.id)
    return [VideoSchemaOut(**video.dict()) for video in videos]
from typing import Any, AsyncIterator, List
from uuid import UUID
from crud.video import CRUDVideo

import loguru
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from sqlalchemy.ext.asyncio.session import AsyncSession

from api.deps.db import get_db, get_redis
from api.deps.nakamal import get_nakamal_or_404
from api.deps.user import current_active_verified_user, current_superuser
from crud.checkin import CRUDCheckin
from crud.image import CRUDImage
from crud.nakamal import CRUDNakamal
from crud.nakamalResource import CRUDNakamalResource
from crud.trip import CRUDTrip
from models.nakamal import Nakamal
from schemas.checkin import CheckinSchemaOut
from schemas.image import ImageSchemaOut
from schemas.trip import TripSchemaOut
from schemas.video import VideoSchemaOut
from schemas.nakamal import (NakamalSchema, NakamalSchemaIn,
                                 NakamalSchemaOut, NakamalSchemaUpdate)

logger = loguru.logger


router = SQLAlchemyCRUDRouter(
    prefix="nakamals",
    tags=["nakamals"],
    schema=NakamalSchema,
    create_schema=NakamalSchemaIn,
    update_schema=NakamalSchemaUpdate,
    db_model=Nakamal,
    db=get_db,
    get_one_route=False,
    get_all_route=False,
    delete_one_route=False,
    delete_all_route=False,
    create_route=[Depends(current_active_verified_user)],
    update_route=False,
)


# @router.post("", response_model=NakamalSchemaOut)
# async def create_one(
#     request: Request,
#     db: AsyncSession = Depends(get_db),
#     user = Depends(current_active_verified_user),
#     *,
#     payload: NakamalSchemaIn,
# ) -> Any:
#     crud_nakamal = CRUDNakamal(db)
#     item = await crud_nakamal.create(payload)
#     return NakamalSchemaOut(**item.dict())


@router.get("", response_model=List[NakamalSchemaOut])
async def get_all(
    db: AsyncSession = Depends(get_db),
) -> Any:
    crud_nakamal = CRUDNakamal(db)
    items = await crud_nakamal.get_multi()
    # TODO load profile
    return [NakamalSchemaOut(**item.dict()) for item in items]


@router.get("/featured", response_model=NakamalSchemaOut)
async def get_featured(
    db: AsyncSession = Depends(get_db),
    redis: AsyncIterator = Depends(get_redis),
) -> Any:
    item_id = await redis.get("featured-nakamal")
    if not item_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Featured nakamal not found.",
        )
    crud_nakamal = CRUDNakamal(db)
    item = await crud_nakamal.get_by_id(item_id.decode())
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nakamal not found.",
        )
    # TODO load profile
    return item


@router.get(
    "/{item_id:uuid}",
    response_model=NakamalSchemaOut,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "detail": "Nakamal not found.",
        },
    },
)
async def get_one(
    db: AsyncSession = Depends(get_db),
    item: NakamalSchema = Depends(get_nakamal_or_404),
) -> NakamalSchemaOut:  
    # crud_image = CRUDImage(db)
    # profile = await crud_image.get_current_nakamal_profile(item.id)
    # item.profile = crud_image.make_src_urls(item.profile)
    # return NakamalSchemaOut(**item.dict())  #, profile=profile)
    return item


@router.put(
    "/{item_id:uuid}",
    response_model=NakamalSchemaOut,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "detail": "Nakamal not found.",
        },
    },
)
async def update_one(
    db: AsyncSession = Depends(get_db),
    user = Depends(current_active_verified_user),
    *,
    item: NakamalSchema = Depends(get_nakamal_or_404),
    payload: NakamalSchemaUpdate,
) -> NakamalSchemaOut:
    crud_nakamal = CRUDNakamal(db)
    # logger.bind(payload=payload.dict()).debug("nakamal update")  # XXX take a look at this again and consider using to trigger alert for me
    item = await crud_nakamal.update(item.id, payload)
    # TODO load profile
    return NakamalSchemaOut(**item.dict())


@router.delete(
    "/{item_id:uuid}",
    response_model=NakamalSchemaOut,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "detail": "Nakamal not found.",
        },
    },
)
async def delete_one(
    db: AsyncSession = Depends(get_db),
    superuser = Depends(current_superuser),
    *,
    item: NakamalSchema = Depends(get_nakamal_or_404),
) -> NakamalSchemaOut:
    # XXX fails when checkins or images or resources exist on the relationships
    crud_nakamal = CRUDNakamal(db)
    # TODO load profile
    item = await crud_nakamal.remove(item.id)
    return NakamalSchemaOut(**item.dict())


@router.put(
    "/{item_id:uuid}/featured",
    response_model=NakamalSchemaOut,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "detail": "Nakamal not found.",
        },
    },
)
async def update_featured(
    redis: AsyncIterator = Depends(get_redis),
    *,
    item: NakamalSchema = Depends(get_nakamal_or_404),
) -> NakamalSchemaOut:
    await redis.set("featured-nakamal", str(item.id))
    # TODO load profile
    return NakamalSchemaOut(**item.dict())


@router.get(
    "/{item_id:uuid}/images",
    response_model=List[ImageSchemaOut],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "detail": "Nakamal not found.",
        },
    },
)
async def get_all_images(
    db: AsyncSession = Depends(get_db),
    *,
    item: NakamalSchema = Depends(get_nakamal_or_404),
) -> List[ImageSchemaOut]:
    crud_image = CRUDImage(db)
    images = await crud_image.get_multi_by_nakamal(item.id)
    return [ImageSchemaOut(**image.dict()) for image in images]


@router.get(
    "/{item_id:uuid}/checkins",
    response_model=List[CheckinSchemaOut],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "detail": "Nakamal not found.",
        },
    },
)
async def get_all_checkins(
    db: AsyncSession = Depends(get_db),
    *,
    item: NakamalSchema = Depends(get_nakamal_or_404),
) -> List[CheckinSchemaOut]:
    crud_checkin = CRUDCheckin(db)
    checkins = await crud_checkin.get_multi_by_nakamal(item.id)
    return [CheckinSchemaOut(**checkin.dict()) for checkin in checkins]


@router.get(
    "/{item_id:uuid}/videos",
    response_model=List[VideoSchemaOut],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "detail": "Nakamal not found.",
        },
    },
)
async def get_all_videos(
    db: AsyncSession = Depends(get_db),
    *,
    item: NakamalSchema = Depends(get_nakamal_or_404),
) -> List[VideoSchemaOut]:
    crud_video = CRUDVideo(db)
    videos = await crud_video.get_multi_by_nakamal(item.id)
    return [VideoSchemaOut(**video.dict()) for video in videos]


@router.get(
    "/{item_id:uuid}/trips",
    response_model=List[TripSchemaOut],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "detail": "Nakamal not found.",
        },
    },
)
async def get_all_trips(
    db: AsyncSession = Depends(get_db),
    *,
    item: NakamalSchema = Depends(get_nakamal_or_404),
) -> List[TripSchemaOut]:
    crud_trip = CRUDTrip(db)
    trips = await crud_trip.get_multi_by_nakamal(item.id)
    return [TripSchemaOut(**trip.dict()) for trip in trips]


@router.put(
    "/{item_id:uuid}/resources/{resource_id:uuid}",
    response_model=NakamalSchemaOut,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "detail": "Nakamal not found.",
        },
    },
)
async def put_one_resource(
    db: AsyncSession = Depends(get_db),
    user = Depends(current_active_verified_user),
    *,
    item: NakamalSchema = Depends(get_nakamal_or_404),
    resource_id: UUID,
) -> NakamalSchemaOut:
    crud_nakamal = CRUDNakamal(db)
    crud_resource = CRUDNakamalResource(db)
    resource = await crud_resource.get_by_id(resource_id)
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nakamal Resource not found."
        )
    r = await crud_resource._get_one(resource.id)
    await crud_nakamal.add_resource(item.id, r)
    item = await crud_nakamal.get_by_id(item.id)
    return NakamalSchemaOut(**item.dict())


@router.delete(
    "/{item_id:uuid}/resources/{resource_id:uuid}",
    response_model=NakamalSchemaOut,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "detail": "Nakamal not found.",
        },
    },
)
async def delete_one_resource(
    db: AsyncSession = Depends(get_db),
    user = Depends(current_active_verified_user),
    *,
    item: NakamalSchema = Depends(get_nakamal_or_404),
    resource_id: UUID,
) -> NakamalSchemaOut:
    crud_nakamal = CRUDNakamal(db)
    crud_resource = CRUDNakamalResource(db)
    resource = await crud_resource.get_by_id(resource_id)
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nakamal Resource not found."
        )
    r = await crud_resource._get_one(resource.id)
    await crud_nakamal.remove_resource(item.id, r)
    item = await crud_nakamal.get_by_id(item.id)
    return NakamalSchemaOut(**item.dict())


@router.put(
    "/{item_id:uuid}/profiles/{image_id:uuid}",
    response_model=NakamalSchemaOut,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "detail": "Nakamal Not Found.",
        },
    },
)
async def put_profile_image(
    db: AsyncSession = Depends(get_db),
    user = Depends(current_active_verified_user),
    *,
    item: NakamalSchema = Depends(get_nakamal_or_404),
    image_id: UUID,
) -> NakamalSchemaOut:
    """Set new nakamal profile image"""    
    # TODO check user is chief to set profie
    # if item.nakamal_id is None:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    #
    crud_image = CRUDImage(db)
    image = await crud_image.get_by_id(image_id)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found."
        )
    if image.nakamal.id != item.id:
        raise HTTPException(
            status_code =status.HTTP_400_BAD_REQUEST, detail="Image is not associated with the nakamal."
        )
    await crud_image.create_nakamal_profile(image)
    crud_nakamal = CRUDNakamal(db)
    item = await crud_nakamal.get_by_id(item.id)
    return NakamalSchemaOut(**item.dict())


@router.delete("/{item_id:uuid}/profiles/{image_id:uuid}")
async def delete_profile_image(
    db: AsyncSession = Depends(get_db),
    user = Depends(current_active_verified_user),
    *,
    item: NakamalSchema = Depends(get_nakamal_or_404),
    image_id: UUID,
) -> NakamalSchemaOut:
    """Remove nakamal profile image."""
    # remove all occurances of image Id from nakamal profile table
    
    crud_image = CRUDImage(db)
    image = await crud_image.get_by_id(image_id)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Image not found."
        )
    await crud_image.remove_nakamal_profile(image.id)    
    return NakamalSchemaOut(**item.dict())
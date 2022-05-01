from typing import Any, AsyncIterator, List
from uuid import UUID

import loguru
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.api.deps.db import get_db, get_redis
from app.api.deps.nakamal import get_nakamal_or_404
from app.api.deps.user import current_active_verified_user, current_superuser
from app.crud.checkin import CRUDCheckin
from app.crud.image import CRUDImage
from app.crud.nakamal import CRUDNakamal
from app.crud.nakamalResource import CRUDNakamalResource
from app.models.nakamal import Nakamal
from app.schemas.checkin import CheckinSchemaOut
from app.schemas.image import ImageSchemaOut
from app.schemas.nakamal import (NakamalSchema, NakamalSchemaIn,
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


@router.get("", response_model=List[NakamalSchemaOut])
async def get_all(
    db: AsyncSession = Depends(get_db),
) -> Any:
    crud_nakamal = CRUDNakamal(db)
    items = await crud_nakamal.get_multi()
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
    item: NakamalSchema = Depends(get_nakamal_or_404),
) -> NakamalSchemaOut:
    return NakamalSchemaOut(**item.dict())


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
    item = await crud_nakamal.delete(item.id)
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
async def get_all_images(
    db: AsyncSession = Depends(get_db),
    *,
    item: NakamalSchema = Depends(get_nakamal_or_404),
) -> List[CheckinSchemaOut]:
    crud_checkin = CRUDCheckin(db)
    checkins = await crud_checkin.get_multi_by_nakamal(item.id)
    return [CheckinSchemaOut(**checkin.dict()) for checkin in checkins]


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

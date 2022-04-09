from typing import Any, List
from uuid import UUID

import loguru
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.api.deps.db import get_db
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
    delete_all_route=False,
    create_route=[Depends(current_active_verified_user)],
    update_route=[Depends(current_active_verified_user)],
    delete_one_route=[Depends(current_superuser)],
)


@router.get("", response_model=List[NakamalSchemaOut])
async def get_all(
    db: AsyncSession = Depends(get_db),
) -> Any:
    crud_nakamal = CRUDNakamal(db)
    items = await crud_nakamal.get_multi()
    return [NakamalSchemaOut(**item.dict()) for item in items]


@router.get("/{item_id}", response_model=NakamalSchemaOut)
async def get_one(db: AsyncSession = Depends(get_db), *, item_id: UUID) -> Any:
    crud_nakamal = CRUDNakamal(db)
    item = await crud_nakamal.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nakamal not found."
        )
    return item


# TODO sort out handling eager loading
@router.put("/{item_id}", response_model=NakamalSchemaOut)
async def update_one(
    db: AsyncSession = Depends(get_db),
    user=Depends(current_active_verified_user),
    *,
    item_id: UUID,
    update_schema: NakamalSchemaUpdate,
) -> Any:
    crud_nakamal = CRUDNakamal(db)
    item = await crud_nakamal.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nakamal not found."
        )

    # logger.bind(payload=update_schema.dict()).debug("nakamal update")
    item = await crud_nakamal.update(item_id, update_schema)
    return NakamalSchemaOut(**item.dict())


@router.delete("/{item_id}", response_model=NakamalSchemaOut)
async def delete_one(
    db: AsyncSession = Depends(get_db),
    user=Depends(current_superuser),
    *,
    item_id: UUID,
) -> Any:
    # XXX fails when checkins or images or resources exist on the relationships
    crud_nakamal = CRUDNakamal(db)
    item = await crud_nakamal.delete(item_id)
    return NakamalSchemaOut(**item.dict())


@router.get("/{item_id}/images", response_model=List[ImageSchemaOut])
async def get_all_images(db: AsyncSession = Depends(get_db), *, item_id: UUID) -> Any:
    crud_nakamal = CRUDNakamal(db)
    item = await crud_nakamal.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nakamal not found."
        )
    crud_image = CRUDImage(db)
    images = await crud_image.get_multi_by_nakamal(item.id)
    return [ImageSchemaOut(**image.dict()) for image in images]


@router.get("/{item_id}/checkins", response_model=List[CheckinSchemaOut])
async def get_all_images(db: AsyncSession = Depends(get_db), *, item_id: UUID) -> Any:
    crud_nakamal = CRUDNakamal(db)
    item = await crud_nakamal.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nakamal not found."
        )
    crud_checkin = CRUDCheckin(db)
    checkins = await crud_checkin.get_multi_by_nakamal(item.id)
    return [CheckinSchemaOut(**checkin.dict()) for checkin in checkins]


@router.put("/{item_id}/resources/{resource_id}", response_model=NakamalSchemaOut)
async def put_one_resource(
    db: AsyncSession = Depends(get_db),
    user=Depends(current_active_verified_user),
    *,
    item_id: UUID,
    resource_id: UUID,
) -> Any:
    crud_nakamal = CRUDNakamal(db)
    item = await crud_nakamal.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nakamal not found."
        )
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


@router.delete("/{item_id}/resources/{resource_id}", response_model=NakamalSchemaOut)
async def delete_one_resource(
    db: AsyncSession = Depends(get_db),
    user=Depends(current_active_verified_user),
    *,
    item_id: UUID,
    resource_id: UUID,
) -> Any:
    crud_nakamal = CRUDNakamal(db)
    item = await crud_nakamal.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nakamal not found."
        )
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

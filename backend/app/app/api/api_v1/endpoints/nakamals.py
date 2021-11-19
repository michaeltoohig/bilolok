from typing import Any, List, Optional
from app.api.api_v1.endpoints.images import get_one
from app.schemas.checkin import CheckinDB

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi_crudrouter import DatabasesCRUDRouter

from app import crud
from app.api.deps import current_active_verified_user, current_superuser
from app.db.session import database
from app.models.nakamal import NakamalTable
from app.schemas.nakamal import NakamalCreate, NakamalDB, NakamalUpdate
from app.schemas.image import ImageDB
from pydantic.types import UUID4


router = DatabasesCRUDRouter(
    prefix="nakamals",
    tags=["nakamals"],
    schema=NakamalDB,
    create_schema=NakamalCreate,
    update_schema=NakamalUpdate,
    table=NakamalTable,
    database=database,
    get_one_route=False,
    get_all_route=False,
    delete_all_route=False,
    create_route=[Depends(current_active_verified_user)],
    update_route=[Depends(current_active_verified_user)],
    delete_one_route=[Depends(current_superuser)],
)


@router.get("", response_model=List[NakamalDB])
async def get_all() -> Any:
    records = await crud.nakamal.get_multi()
    return records


@router.get("/{item_id}", response_model=NakamalDB)
async def get_one(item_id: UUID4) -> Any:
    # TODO nakamal dependency
    record = await crud.nakamal.get(item_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nakamal not found.")
    return record
    

@router.get("/{item_id}/images", response_model=List[ImageDB])
async def get_all_images(
    item_id: UUID4
) -> Any:
    # TODO nakamal dependency
    record = await crud.nakamal.get(item_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nakamal not found.")
    images = await crud.image.get_multi_by_nakamal(record.id)
    return images


@router.get("/{item_id}/checkins", response_model=List[CheckinDB])
async def get_all_checkins(
    item_id: UUID4,
) -> Any:
    # TODO nakamal dependency
    record = await crud.nakamal.get(item_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nakamal not found.")
    checkins = await crud.checkin.get_multi_by_nakamal(record.id)
    return checkins
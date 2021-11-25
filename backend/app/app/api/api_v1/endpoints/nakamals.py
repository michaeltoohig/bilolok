from typing import Any, List, Optional
from app.api.api_v1.endpoints.images import get_one
from app.api.deps.db import get_db

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi_crudrouter import SQLAlchemyCRUDRouter

from app.crud.nakamal import CRUDNakamal
from app.crud.image import CRUDImage
from app.models.nakamal import Nakamal
from app.api.deps.user import current_active_verified_user, current_superuser
from app.schemas.nakamal import NakamalSchemaIn, NakamalSchema, NakamalSchemaOut
from app.schemas.image import ImageSchema, ImageSchemaOut
from sqlalchemy.ext.asyncio.session import AsyncSession


router = SQLAlchemyCRUDRouter(
    prefix="nakamals",
    tags=["nakamals"],
    schema=NakamalSchema,
    create_schema=NakamalSchemaIn,
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
async def get_one(
    db: AsyncSession = Depends(get_db),
    *,
    item_id: str
) -> Any:
    crud_nakamal = CRUDNakamal(db)
    item = await crud_nakamal.get_by_id(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nakamal not found.")
    return item
    

@router.get("/{item_id}/images", response_model=List[ImageSchemaOut])
async def get_all_images(
    db: AsyncSession = Depends(get_db),
    *,
    item_id: str
) -> Any:
    crud_nakamal = CRUDNakamal(db)
    item = await crud_nakamal.get_by_id(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nakamal not found.")
    crud_image = CRUDImage(db)
    images = await crud_image.get_multi_by_nakamal(item.id)
    return [ImageSchemaOut(**image.dict()) for image in images]

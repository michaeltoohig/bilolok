from typing import Any, List, Optional

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi_crudrouter import DatabasesCRUDRouter

from app import crud
from app.api.deps import current_active_verified_user, current_superuser
from app.db.session import database
from app.models.nakamal import NakamalTable
from app.schemas.nakamal import NakamalCreate, NakamalDB, NakamalUpdate
from app.schemas.image import ImageDB


router = DatabasesCRUDRouter(
    prefix="nakamals",
    tags=["nakamals"],
    schema=NakamalDB,
    create_schema=NakamalCreate,
    update_schema=NakamalUpdate,
    table=NakamalTable,
    database=database,
    # Disable delete_all endpoint
    delete_all_route=False,
    # Dependencies for endpoints
    create_route=[Depends(current_active_verified_user)],
    update_route=[Depends(current_active_verified_user)],
    delete_one_route=[Depends(current_superuser)],
)


@router.get("/{item_id}/images", response_model=List[ImageDB])
async def get_all_images(
    item_id: str
) -> Any:
    record = await crud.nakamal.get(item_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nakamal not found.")
    nakamal = NakamalDB(**record)
    images = await crud.image.get_multi_by_nakamal(nakamal.id)
    for image in images:
        image.src = crud.image.make_src(image, height=1080, width=1920, full_fit_in=True)
        image.msrc = crud.image.make_src(image, height=32, width=32, full_fit_in=True)
        image.thumbnail = crud.image.make_src(image, height=200, width=200)
    return images

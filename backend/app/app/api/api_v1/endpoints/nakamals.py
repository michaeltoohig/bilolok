from typing import Any, List, Optional
from uuid import UUID

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi_crudrouter import OrmarCRUDRouter

from app import crud, models
from app.api.deps import current_active_verified_user, current_superuser
# from app.models.image import Image
# from app.models.nakamal import Nakamal


router = OrmarCRUDRouter(
    schema=models.Nakamal,
    prefix="nakamals",
    tags=["nakamals"],
    get_one_route=False,
    get_all_route=False,
    delete_all_route=False,
    create_route=[Depends(current_active_verified_user)],
    update_route=[Depends(current_active_verified_user)],
    delete_one_route=[Depends(current_superuser)],
)


# TODO get_one endpoint with additional logic added to
#  include realtime checkin count. Perhaps recent checkins


@router.get("", response_model=List[models.Nakamal])
async def get_all() -> Any:
    items = await crud.nakamal.get_multi()
    return items


@router.get("/{item_id}", response_model=models.Nakamal)
async def get_one(item_id: UUID) -> Any:
    # TODO nakamal dependency
    item = await crud.nakamal.get(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nakamal not found.")
    return item
    

@router.get("/{item_id}/images", response_model=List[models.Image])
async def get_all_images(
    item_id: UUID
) -> Any:
    # TODO nakamal dependency
    item = await crud.nakamal.get(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nakamal not found.")
    images = await crud.image.get_multi_by_nakamal(item.id)
    return images


@router.get("/{item_id}/checkins", response_model=List[models.Checkin])
async def get_all_checkins(
    item_id: UUID,
) -> Any:
    # TODO nakamal dependency
    item = await crud.nakamal.get(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nakamal not found.")
    checkins = await crud.checkin.get_multi_by_nakamal(item.id)
    return checkins
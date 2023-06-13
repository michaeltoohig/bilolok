from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps.db import get_db
from crud.image import CRUDImage
from db.errors import DoesNotExist
from schemas.image import ImageSchema


async def get_image_or_404(
    db: AsyncSession = Depends(get_db),
    *,
    item_id: UUID,
) -> ImageSchema:
    crud_image = CRUDImage(db)
    try:
        item = await crud_image.get_by_id(item_id)
        return item
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.db import get_db
from app.crud.video import CRUDVideo
from app.db.errors import DoesNotExist
from app.schemas.video import VideoSchema


async def get_video_or_404(
    db: AsyncSession = Depends(get_db),
    *,
    item_id: UUID,
) -> VideoSchema:
    crud_video = CRUDVideo(db)
    try:
        item = await crud_video.get_by_id(item_id)
        return item
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

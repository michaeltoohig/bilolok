from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.deps.db import get_db
from crud.checkin import CRUDCheckin
from db.errors import DoesNotExist
from schemas.checkin import CheckinSchema


async def get_checkin_or_404(
    db: AsyncSession = Depends(get_db),
    *,
    item_id: UUID,
) -> CheckinSchema:
    crud_checkin = CRUDCheckin(db)
    try:
        item = await crud_checkin.get_by_id(item_id)
        return item
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
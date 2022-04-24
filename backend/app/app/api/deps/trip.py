from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps.db import get_db
from app.crud.trip import CRUDTrip
from app.db.errors import DoesNotExist
from app.schemas.trip import TripSchema


async def get_trip_or_404(
    db: AsyncSession = Depends(get_db),
    *,
    item_id: UUID,
) -> TripSchema:
    crud_trip = CRUDTrip(db)
    try:
        item = await crud_trip.get_by_id(item_id)
        return item
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
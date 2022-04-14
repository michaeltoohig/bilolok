from datetime import datetime, timedelta, timezone
from typing import Any, List

from fastapi import Depends, Query, status
from fastapi.exceptions import HTTPException
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from sqlalchemy.ext.asyncio.session import AsyncSession
from pydantic import UUID4

from app.api.deps.db import get_db
from app.api.deps.user import current_active_verified_user, current_superuser
from app.crud.trip import CRUDTrip
from app.models.trip import Trip
from app.models.user import User
from app.schemas.trip import (TripSchema, TripSchemaIn,
                                 TripSchemaOut)

router = SQLAlchemyCRUDRouter(
    prefix="trips",
    tags=["trips"],
    schema=TripSchema,
    create_schema=TripSchemaIn,
    db_model=Trip,
    db=get_db,
    get_one_route=False,
    get_all_route=False,
    create_route=False,
    update_route=False,
    delete_all_route=False,
    delete_one_route=False,
)


@router.get("", response_model=List[TripSchemaOut])
async def get_all(
    db: AsyncSession = Depends(get_db),
    *,
    recent: bool = Query(False),
    skip: int = 0,
    limit: int = 100,
) -> List[TripSchemaOut]:
    crud_trip = CRUDTrip(db)
    if recent:
        items = await crud_trip.get_recent()
        return [TripSchemaOut(**item.dict()) for item in items]
    else:
        items = await crud_trip.get_multi(skip=skip, limit=limit)
        return [TripSchemaOut(**item.dict()) for item in items]


@router.post(
    "",
    response_model=TripSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_one(
    db: AsyncSession = Depends(get_db),
    *,
    in_schema: TripSchemaIn,
    user: User = Depends(current_active_verified_user),
) -> Any:
    """Trip to a nakamal"""
    crud_trip = CRUDTrip(db)
    trip = await crud_trip.create(in_schema, user_id=user.id)
    return trip


@router.get("/{item_id:uuid}", response_model=TripSchema)
async def get_one(
    db: AsyncSession = Depends(get_db),
    *,
    item_id: UUID4
) -> Any:
    """Trip to a nakamal"""
    crud_trip = CRUDTrip(db)
    trip = await crud_trip.get_by_id(item_id)
    return trip


@router.delete("/{item_id:uuid}", response_model=TripSchema)
async def delete_one(
    db: AsyncSession = Depends(get_db),
    *,
    item_id: UUID4,
    user: User = Depends(current_superuser),
) -> Any:
    """Delete a trip to a nakamal"""
    crud_trip = CRUDTrip(db)
    trip = await crud_trip.delete(item_id)
    return trip

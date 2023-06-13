from datetime import datetime, timedelta, timezone
from typing import Any, List
from api.deps.trip import get_trip_or_404

from fastapi import Depends, Query, status
from fastapi.exceptions import HTTPException
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from sqlalchemy.ext.asyncio.session import AsyncSession
from pydantic import UUID4

from api.deps.db import get_db
from api.deps.user import current_active_verified_user, current_superuser
from crud.trip import CRUDTrip
from models.trip import Trip
from models.user import User
from schemas.trip import (TripSchema, TripSchemaIn,
                                 TripSchemaOut)

# TODO remove crud router
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
    else:
        items = await crud_trip.get_multi(skip=skip, limit=limit)
    return [TripSchemaOut(**item.dict()) for item in items]


@router.get(
    "/{item_id:uuid}",
    response_model=TripSchemaOut,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "detail": "Trip not found.",
        },
    },
)
async def get_one(
    item: TripSchema = Depends(get_trip_or_404),
) -> TripSchemaOut:
    """Trip to a nakamal"""
    return TripSchemaOut(**item.dict())


@router.post(
    "",
    response_model=TripSchemaOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_one(
    db: AsyncSession = Depends(get_db),
    *,
    payload: TripSchemaIn,
    user: User = Depends(current_active_verified_user),
) -> TripSchemaOut:
    """Trip to a nakamal"""
    crud_trip = CRUDTrip(db)
    item = await crud_trip.create(payload, user_id=user.id)
    return TripSchemaOut(**item.dict())


@router.delete(
    "/{item_id:uuid}",
    response_model=TripSchemaOut,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "detail": "User does not have permission to delete this trip."
        },
        status.HTTP_404_NOT_FOUND: {
            "detail": "Trip not found.",
        },
    },
)
async def delete_one(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_verified_user),
    *,
    item: TripSchema = Depends(get_trip_or_404),
) -> Any:
    """Delete a trip to a nakamal"""
    if not user.is_superuser:
        if user.id != item.user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    crud_trip = CRUDTrip(db)
    item = await crud_trip.delete(item.id)
    return TripSchemaOut(**item.dict())

from datetime import datetime, timedelta, timezone
from typing import Any, List
from app.api.deps.checkin import get_checkin_or_404

from fastapi import Depends, Query, status
from fastapi.exceptions import HTTPException
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.api.deps.db import get_db
from app.api.deps.user import current_active_verified_user, current_superuser
from app.crud.checkin import CRUDCheckin
from app.models.checkin import Checkin
from app.models.user import User
from app.schemas.checkin import (CheckinSchema, CheckinSchemaIn,
                                 CheckinSchemaOut)

router = SQLAlchemyCRUDRouter(
    prefix="checkins",
    tags=["checkins"],
    schema=CheckinSchema,
    create_schema=CheckinSchemaIn,
    db_model=Checkin,
    db=get_db,
    get_all_route=False,
    create_route=False,
    update_route=False,
    delete_all_route=False,
    delete_one_route=False,
)


@router.get("", response_model=List[CheckinSchemaOut])
async def get_all(
    db: AsyncSession = Depends(get_db),
    *,
    recent: bool = Query(False),
    skip: int = 0,
    limit: int = 100,
) -> List[CheckinSchemaOut]:
    crud_checkin = CRUDCheckin(db)
    if recent:
        items = await crud_checkin.get_recent()
    else:
        items = await crud_checkin.get_multi(skip=skip, limit=limit)
    return [CheckinSchemaOut(**item.dict()) for item in items]


@router.post(
    "",
    response_model=CheckinSchemaOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_one(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_verified_user),
    *,
    payload: CheckinSchemaIn,
) -> Any:
    """Checkin to a nakamal.

    Considerations (to be reviewed):
     - Check user does not repeatedly checkin to the same nakamal in a short time frame
     - Check user does not bunny hop between many near by locations to collect checkins
     - Perhaps require lat/lng to allow repeated successive checkins to the same nakamal
         i.e. the user remains at one location for an extended period of time.
         Or only allow one checkin per visit regardless of duration (see bunny hop concern above)
          - set a limit on successive checkins during an extended session/stay at one nakamal
          - feature: if phone GPS is on automatically query to continue checkin
     - Allow user to checkin to same nakamal in succession if enough time elapses
         i.e. checkin to same nakamal each day and no other checkins inbetween

    I believe a single check-in per visit is easiest and user-friendly design, just look out
    for bunny hoppers and things should be okay.
    """
    now = datetime.now(tz=timezone.utc)
    # TODO check user has not hit some checkin count threshold for the day - no bots or automated checkin spam
    # Check user's latest checkin is not the same nakamal - no double checkins
    crud_checkin = CRUDCheckin(db)
    last_checkin = await crud_checkin.get_last_by_user(user.id, exclude_private=False)
    if last_checkin:
        same_nakamal = last_checkin.nakamal.id == payload.nakamal_id
        threshold = last_checkin.created_at + timedelta(hours=12)  # XXX hardcoded value
        within_threshold = now < threshold
        if same_nakamal and within_threshold:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You already checked-in to this nakamal.",
            )
    # Check user's latest checkin at this nakamal was atleast X minutes ago - no double checkins by hopping between two nakamals
    last_nakamal_checkin = await crud_checkin.get_last_by_user(
        user.id, nakamal_id=payload.nakamal_id, exclude_private=False
    )
    if last_nakamal_checkin:
        threshold = last_nakamal_checkin.created_at + timedelta(
            minutes=15
        )  # XXX hardcoded value
        if now < threshold:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You already checked-in to this nakamal recently.",
            )
    # Check user has not checked in more than the threshold for a single day
    checkin_threshold = 3  # XXX hardcoded value
    recent_nakamal_checkins = await crud_checkin.get_multi_by_user(
        user.id,
        limit=checkin_threshold,
        nakamal_id=payload.nakamal_id,
        exclude_private=False,
    )
    threshold = datetime.now(tz=timezone.utc) - timedelta(hours=12)
    count = len(
        list(filter(lambda c: c.created_at >= threshold, recent_nakamal_checkins))
    )
    if count > checkin_threshold:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already checked-in to this nakamal too many times today.",
        )
    # Create checkin
    checkin = await crud_checkin.create(payload, user_id=user.id)
    return CheckinSchemaOut(**checkin.dict())


@router.delete(
    "/{item_id:uuid}",
    response_model=CheckinSchemaOut,
    responses={
        status.HTTP_403_FORBIDDEN: {
            "detail": "User does not have permission to delete this check-in."
        },
        status.HTTP_404_NOT_FOUND: {
            "detail": "Check-in not found.",
        },
    },
)
async def delete_one(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_verified_user),
    *,
    item: CheckinSchema = Depends(get_checkin_or_404),
) -> Any:
    """Delete a check-in at a nakamal"""
    if not user.is_superuser:
        if user.id != item.user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    crud_checkin = CRUDCheckin(db)
    item = await crud_checkin.delete(item.id)
    return CheckinSchemaOut(**item.dict())

from typing import Any, List, Optional
from datetime import datetime, timedelta, timezone

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.api.deps.db import get_db
from app.api.deps.user import current_superuser, current_active_verified_user, current_active_user
from app.crud.checkin import CRUDCheckin
from app.models.checkin import Checkin
from app.models.user import User
from app.schemas.checkin import CheckinSchemaIn, CheckinSchema, CheckinSchemaOut


router = SQLAlchemyCRUDRouter(
    prefix="checkins",
    tags=["checkins"],
    schema=CheckinSchema,
    create_schema=CheckinSchemaIn,
    db_model=Checkin,
    db=get_db,
    create_route=False,
    delete_all_route=False,
    delete_one_route=[Depends(current_superuser)],
)


# TODO remove this endpoint after async sqlalchemy crudrouter is merged into project 
# see: https://github.com/awtkns/fastapi-crudrouter/pull/121
@router.get("", response_model=List[CheckinSchemaOut])
async def get_all(
    db: AsyncSession = Depends(get_db),
    *,
    skip: Optional[int] = 0,
    limit: Optional[int] = 100,
) -> Any:
    crud_checkin = CRUDCheckin(db)
    checkins = await crud_checkin.get_multi()  #skip=skip, limit=limit)
    return [CheckinSchemaOut(**checkin.dict()) for checkin in checkins]


@router.get("/me", response_model=List[CheckinSchemaOut])
async def get_all_me(
    db: AsyncSession = Depends(get_db),
    *,
    user: User = Depends(current_active_user)
) -> Any:
    pass


@router.post("", response_model=CheckinSchemaOut)
async def create_one(
    db: AsyncSession = Depends(get_db),
    *,
    schema_in: CheckinSchemaIn,
    user: User = Depends(current_active_verified_user)
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
    import pdb; pdb.set_trace()
    last_checkin = await crud_checkin.get_last_by_user(user.id, exclude_private=False)
    if last_checkin:
        same_nakamal = last_checkin.nakamal.id == schema_in.nakamal_id
        threshold = last_checkin.created_at + timedelta(hours=12)  # XXX hardcoded value
        within_threshold = now < threshold
        if same_nakamal and within_threshold:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You already checked-in to this nakamal."
            )
    # Check user's latest checkin at this nakamal was atleast 30 minutes ago - no double checkins by hopping between two nakamals
    last_nakamal_checkin = await crud_checkin.get_last_by_user(user.id, nakamal_id=schema_in.nakamal, exclude_private=False)
    if last_nakamal_checkin:
        threshold = last_nakamal_checkin.created_at + timedelta(minutes=15)  # XXX hardcoded value
        if now < threshold:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You already checked-in to this nakamal recently."
            )
    # Check user has not checked in more than the threshold for a single day
    count_recent_nakamal_checkins = await crud_checkin.get_multi_by_user(user.id, exclude_private=False, nakamal=schema_in.nakamal)
    if len(count_recent_nakamal_checkins) > 3:  # XXX hardcoded value
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already checked-in to this nakamal too many times today."
        )
    # Create checkin
    checkin = await crud_checkin.create(**schema_in.dict(), user=user.id)
    checkin.user.load()
    return checkin
from typing import Any
from datetime import datetime, timedelta, timezone

from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi_crudrouter import DatabasesCRUDRouter

from app import crud, models
from app.api.deps import current_superuser, current_active_verified_user
from app.db.session import database
from app.models.checkin import CheckinTable
from app.schemas.checkin import CheckinCreate, CheckinUpdate, CheckinDB
from starlette.status import HTTP_400_BAD_REQUEST


router = DatabasesCRUDRouter(
    prefix="checkins",
    tags=["checkins"],
    schema=CheckinDB,
    create_schema=CheckinCreate,
    update_schema=CheckinUpdate,
    table=CheckinTable,
    database=database,
    create_route=False,
    delete_all_route=False,
    delete_one_route=[Depends(current_superuser)],
)


@router.post("", response_model=CheckinDB)
async def create_one(
    obj_in: CheckinCreate,
    user: models.User = Depends(current_active_verified_user)
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
    # TODO check user has not hit some checkin count threshold for the day - no bots or automated checkins
    # Check user's latest checkin is not the same nakamal - no double checkins 
    last_checkin = await crud.checkin.get_last_by_user(user.id)
    if last_checkin:
        same_nakamal = last_checkin.nakamal_id == obj_in.nakamal_id
        threshold = last_checkin.created_at + timedelta(hours=12)  # XXX hardcoded value
        within_threshold = now < threshold
        if same_nakamal and within_threshold:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You already checked-in to this nakamal."
            )
    # Check user's latest checkin at this nakamal was atleast 30 minutes ago - no double checkins by hopping between two nakamals
    last_nakamal_checkin = await crud.checkin.get_last_by_user(user.id, nakamal_id=obj_in.nakamal_id)
    if last_nakamal_checkin:
        threshold = last_nakamal_checkin.created_at + timedelta(minutes=15)  # XXX hardcoded value
        if now < threshold:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You already checked-in to this nakamal recently."
            )
    # Check user has not checked in more than the threshold for a single day
    count_recent_nakamal_checkins = await crud.checkin.get_recent_by_nakamal(obj_in.nakamal_id, user_id=user.id)
    if len(count_recent_nakamal_checkins) > 3:  # XXX hardcoded value
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="You already checked-in to this nakamal too many times today."
        )
    
    obj_in.user_id = user.id
    checkin = await crud.checkin.create(obj_in=obj_in)
    return checkin

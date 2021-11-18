from typing import Any

from fastapi import Depends
from fastapi_crudrouter import DatabasesCRUDRouter

from app import models
from app.api.deps import current_superuser, current_active_verified_user
from app.db.session import database
from app.models.checkin import CheckinTable
from app.schemas.checkin import CheckinCreate, CheckinUpdate, CheckinDB


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
    user: models.User = Depends(current_active_verified_user)
) -> Any:
    pass

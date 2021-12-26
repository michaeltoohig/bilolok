from app.api.deps.db import get_db

from fastapi import Depends
from fastapi_crudrouter import SQLAlchemyCRUDRouter

from app.models.nakamal import NakamalArea
from app.api.deps.user import current_superuser, current_active_verified_user
from app.schemas.nakamal import NakamalAreaSchemaIn, NakamalAreaSchemaOut


router = SQLAlchemyCRUDRouter(
    prefix="nakamal-areas",
    tags=["nakamals"],
    schema=NakamalAreaSchemaOut,
    create_schema=NakamalAreaSchemaIn,
    db_model=NakamalArea,
    db=get_db,
    get_one_route=False,
    delete_all_route=False,
    create_route=[Depends(current_active_verified_user)],
    update_route=[Depends(current_superuser)],
    delete_one_route=[Depends(current_superuser)],
)

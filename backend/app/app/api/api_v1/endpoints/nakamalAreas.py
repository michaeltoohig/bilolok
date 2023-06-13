from fastapi import Depends
from fastapi_crudrouter import SQLAlchemyCRUDRouter

from api.deps.db import get_db
from api.deps.user import current_active_verified_user, current_superuser
from models.nakamal import NakamalArea
from schemas.nakamal import NakamalAreaSchemaIn, NakamalAreaSchemaOut

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

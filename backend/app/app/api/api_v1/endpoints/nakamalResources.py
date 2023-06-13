from fastapi import Depends
from fastapi_crudrouter import SQLAlchemyCRUDRouter

from api.deps.db import get_db
from api.deps.user import current_superuser
from models.nakamal import NakamalResource
from schemas.nakamal import (NakamalResourceSchemaIn,
                                 NakamalResourceSchemaOut)

router = SQLAlchemyCRUDRouter(
    prefix="nakamal-resources",
    tags=["nakamals"],
    schema=NakamalResourceSchemaOut,
    create_schema=NakamalResourceSchemaIn,
    db_model=NakamalResource,
    db=get_db,
    get_one_route=False,
    delete_all_route=False,
    create_route=[Depends(current_superuser)],
    update_route=[Depends(current_superuser)],
    delete_one_route=[Depends(current_superuser)],
)

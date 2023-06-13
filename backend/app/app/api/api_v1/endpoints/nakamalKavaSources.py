from fastapi import Depends
from fastapi_crudrouter import SQLAlchemyCRUDRouter

from api.deps.db import get_db
from api.deps.user import current_superuser
from models.nakamal import NakamalKavaSource
from schemas.nakamal import (NakamalKavaSourceSchemaIn,
                                 NakamalKavaSourceSchemaOut)

router = SQLAlchemyCRUDRouter(
    prefix="nakamal-kava-sources",
    tags=["nakamals"],
    schema=NakamalKavaSourceSchemaOut,
    create_schema=NakamalKavaSourceSchemaIn,
    db_model=NakamalKavaSource,
    db=get_db,
    get_one_route=False,
    delete_all_route=False,
    create_route=[Depends(current_superuser)],
    update_route=[Depends(current_superuser)],
    delete_one_route=[Depends(current_superuser)],
)

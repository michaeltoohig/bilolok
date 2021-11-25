from typing import Any, List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.user import CRUDUser
from app.api.deps.db import get_db
from app.api.deps.user import current_superuser
from app.core.users import fastapi_users
from app.schemas.user import UserSchema

router = fastapi_users.get_users_router()


@router.get("", response_model=List[UserSchema], dependencies=[Depends(current_superuser)])
async def get_all(
    db: AsyncSession = Depends(get_db)
) -> Any:
    crud_user = CRUDUser(db)
    items = await crud_user.get_multi()
    return [UserSchema(**item.dict()) for item in items]

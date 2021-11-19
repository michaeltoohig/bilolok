from typing import Any, List

from fastapi import Depends

from app.api.deps import current_superuser
from app.core.users import fastapi_users, get_user_manager
from app.schemas.user import UserDB

router = fastapi_users.get_users_router()


@router.get("", response_model=List[UserDB], dependencies=[Depends(current_superuser)])
async def get_all(user_manager = Depends(get_user_manager)) -> Any:
    users = await user_manager.get_multi()
    return users

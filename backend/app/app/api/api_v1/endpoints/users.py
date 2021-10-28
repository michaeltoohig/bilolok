from typing import Any, List

from fastapi import Depends, BackgroundTasks, Request
from sqlalchemy import update

from app import crud, models
from app.api.deps import current_superuser
from app.api.tasks import on_after_register, after_verification_request
from app.core.users import fastapi_users
from app.db.session import database
from app.schemas.user import User, UserCreate, UserDB, UserUpdate

router = fastapi_users.get_users_router()


@router.get("", response_model=List[User], dependencies=[Depends(current_superuser)])
async def read_users() -> Any:
    query = models.User.select()
    return await database.fetch_all(query)


@router.post("", response_model=User, dependencies=[Depends(current_superuser)])
async def create_user(
    request: Request,
    *,
    background_tasks: BackgroundTasks,
    UserIn: UserCreate,
) -> Any:
    user = await fastapi_users.create_user(UserIn)

    await on_after_register(user, request)
    # background_tasks.add_task(after_verification_request)  # needs token
    
    return user


@router.put("/{item_id}", response_model=User, dependencies=[Depends(current_superuser)])
async def update_user(
    request: Request,
    item_id: str,
    UserIn: UserUpdate,
) -> Any:
    # await database.fetch_one(update_stmt)
    # user = await database.fetch_one(models.User.select().where(models.User.c.id == item_id))

    user = await crud.user.update(item_id, obj_in=UserIn)
    # await on_after_register(UserDB(**{**user}), request)

    return user
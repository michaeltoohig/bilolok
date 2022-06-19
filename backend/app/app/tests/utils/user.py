from typing import Dict

from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.orm import Session

# from app import crud
from app.core.config import settings
# from app.models.user import User
# from app.schemas.user import UserCreate, UserUpdate
from app.tests.utils.utils import random_email, random_lower_string
from sqlalchemy.ext.asyncio import AsyncSession


async def user_authentication_headers(
    *, client: AsyncClient, email: str, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password}
    r = await client.post("/auth/jwt/login", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


# def create_random_user(db: Session) -> User:
#     email = random_email()
#     password = random_lower_string()
#     user_in = UserCreate(username=email, email=email, password=password)
#     user = crud.user.create(db=db, obj_in=user_in)
#     return user


# async def create_random_user(db_session: AsyncSession):
#     username = random_lower_string()
#     email = random_email()
#     password = 'password'
#     user = User(
#         username=username, 
#         email=email, 
#         password=password, 
#         active=active, 
#         email_validation_date=email_validation_date, 
#         roles=roles
#     )
#     db_session.session.add(user)
#     db_session.session.commit()
#     db_session.session.refresh(user)
#     return user


# def authentication_token_from_email(
#     *, client: TestClient, email: str, db: Session
# ) -> Dict[str, str]:
#     """
#     Return a valid token for the user with given email.
#     If the user doesn't exist it is created first.
#     """
#     password = random_lower_string()
#     user = crud.user.get_by_email(db, email=email)
#     if not user:
#         user_in_create = UserCreate(username=email, email=email, password=password)
#         user = crud.user.create(db, obj_in=user_in_create)
#     else:
#         user_in_update = UserUpdate(password=password)
#         user = crud.user.update(db, db_obj=user, obj_in=user_in_update)

#     return user_authentication_headers(client=client, email=email, password=password)


import contextlib

from app.schemas.user import UserCreate
from app.core.users import get_user_manager, get_user_db, get_async_session
from fastapi_users.manager import UserAlreadyExists

get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_user(
    email: str,
    password: str,
    is_active: bool = True,
    is_verified: bool = True,
    is_superuser: bool = False,
):
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    user = await user_manager.create(
                        UserCreate(
                            email=email,
                            password=password,
                            is_active=is_active,
                            is_verified=is_verified,
                            is_superuser=is_superuser,
                        ),
                    )
                    print(f"User created {user}")
    except UserAlreadyExists:
        print(f"User {email} already exists")


async def create_random_user():
    email = random_email()
    password = "password"
    await create_user(email, password)
    return email, password

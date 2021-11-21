from typing import List, Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import OrmarUserDatabase

# from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from app.core.config import settings
from app.core.mail import mail, MessageSchema
from app.db.session import database
from app.models.user import User as UserModel
from app.schemas.user import User, UserCreate, UserUpdate, UserDB


class UserManager(BaseUserManager[UserCreate, User]):
    user_db_model = User
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY

    async def get_multi(self) -> List[User]:
        users = await self.user_db.get_multi()
        return users

    async def on_after_register(self, user: User, request: Optional[Request] = None) -> None:
        print(f"User {user.id} has registered.")
        message = MessageSchema(
            subject="Welcome to Bilolok!",
            recipients=[user.email],
            body="Thanks for joining! You can also join our Facebook group to give feedback and suggest improvements for Bilolok."
        )
        await mail.send_message(message)
    
    async def on_after_forgot_password(self, user: User, token: str, request: Optional[Request] = None) -> None:
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(self, user: User, token: str, request: Optional[Request] = None) -> None:
        print(f"Verification requested for user {user.id}. Verification token: {token}")


jwt_authentication = JWTAuthentication(
    secret=settings.SECRET_KEY,
    lifetime_seconds=3600,
    tokenUrl="/api/v1/auth/jwt/login",
    token_audience=[f"{settings.PROJECT_SLUG}:auth"]
)


class MyOrmarUserDatabase(OrmarUserDatabase):
    async def get_multi(self) -> List[UserDB]:
        return await self.model.objects.all()
        # query = self.users.select()
        # users = await self.database.fetch_all(query)
        # return [await self._make_user(user) for user in users]


async def get_user_db():
    yield MyOrmarUserDatabase(UserDB, UserModel)


async def get_user_manager(user_db: MyOrmarUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers(
    get_user_manager,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)
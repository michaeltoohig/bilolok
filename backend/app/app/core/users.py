from fastapi_users import FastAPIUsers
from fastapi_users.db import SQLAlchemyUserDatabase

from app.core.security import jwt_authentication
from app.db.session import database
from app.models.user import User as UserTable
from app.schemas.user import User, UserCreate, UserUpdate, UserDB


users = UserTable.__table__
user_db = SQLAlchemyUserDatabase(UserDB, database, users)

fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)
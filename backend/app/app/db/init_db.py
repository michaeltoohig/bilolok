from sqlalchemy.orm import Session

# from app import crud
from app.core.config import settings
from app.db.session import async_engine, async_session
from app.core.users import fastapi_users
from app.schemas.user import UserCreate

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQLAlchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


async def init_db(db: Session) -> None:
    async with async_engine.begin() as connection:
        async with async_session(bind=connection) as session:

            try:
                superuser = await fastapi_users.create_user(
                    UserCreate(
                        email=settings.FIRST_SUPERUSER,
                        password=settings.FIRST_SUPERUSER_PASSWORD,
                        is_active=True,
                        is_verified=True,
                        is_superuser=True,
                    )
                )
            except:
                pass  # user already exists

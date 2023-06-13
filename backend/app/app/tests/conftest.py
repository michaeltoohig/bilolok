from typing import  AsyncGenerator, Callable, Generator

import asyncio
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from api.deps.user import current_active_user, current_active_verified_user, current_superuser
from core.config import settings
import app.db.base  # noqa
from db.base_class import Base
from db.session import async_session
from schemas.user import UserDB


@pytest_asyncio.fixture(scope="session")
def event_loop(request) -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


engine = create_async_engine(
    "postgresql+asyncpg://user:password@localhost:5433/test_data",
    echo=False,
)


@pytest_asyncio.fixture()
async def db_session() -> AsyncSession:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
        async with async_session(bind=connection) as session:
            yield session
            await session.flush()
            await session.rollback()


@pytest_asyncio.fixture()
def override_get_db(db_session: AsyncSession) -> Callable:
    async def _override_get_db():
        yield db_session
    return _override_get_db


@pytest_asyncio.fixture()
def app(override_get_db: Callable) -> FastAPI:
    from api.deps.db import get_db
    from main import app

    app.dependency_overrides[get_db] = override_get_db
    return app


@pytest_asyncio.fixture()
async def client(app: FastAPI) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url=f"http://test{settings.API_V1_STR}") as ac:
        yield ac


# Below feels wrong but follows https://github.com/fastapi-users/fastapi-users/discussions/671
# I believe I would prefer more explicit `get_user_auth_headers` util in each test


active_user = UserDB(
    email="user@example.com",
    hashed_password="aaa",
    is_active=True,
    is_verified=False,
    is_superuser=False,
)


active_verified_user = UserDB(
    email="user@example.com",
    hashed_password="aaa",
    is_active=True,
    is_verified=True,
    is_superuser=False,
)


super_user = UserDB(
    email="user@example.com",
    hashed_password="aaa",
    is_active=True,
    is_verified=True,
    is_superuser=True,
)


@pytest_asyncio.fixture()
async def not_verified_user_client(app: FastAPI) -> AsyncGenerator:
    app.dependency_overrides[current_active_user] = lambda: active_user
    app.dependency_overrides[current_active_verified_user] = lambda: active_user
    app.dependency_overrides[current_superuser] = lambda: active_user
    async with AsyncClient(app=app, base_url=f"http://test/{{ setttings.API_V1_STR }}") as ac:
        yield ac


@pytest_asyncio.fixture()
async def user_client(app: FastAPI) -> AsyncGenerator:
    app.dependency_overrides[current_active_user] = lambda: active_verified_user
    app.dependency_overrides[current_active_verified_user] = lambda: active_verified_user
    app.dependency_overrides[current_superuser] = lambda: active_verified_user
    async with AsyncClient(app=app, base_url=f"http://test/{{ setttings.API_V1_STR }}") as ac:
        yield ac


@pytest_asyncio.fixture()
async def superuser_client(app: FastAPI) -> AsyncGenerator:
    app.dependency_overrides[current_active_user] = lambda: super_user
    app.dependency_overrides[current_active_verified_user] = lambda: super_user
    app.dependency_overrides[current_superuser] = lambda: super_user
    async with AsyncClient(app=app, base_url=f"http://test/{{ setttings.API_V1_STR }}") as ac:
        yield ac

"""FastAPI Users database adapter for SQLAlchemy + encode/databases."""

"""
Taken from https://github.com/BPL-Development-Team/fastapi-users-db-sqlalchemy-asyncpg
The official FastAPI-Users project still depends on `encode/databases` for
async support for SQLAlchemy. However, with the release of SQLAlchemy version
1.4 `encode/databases` package becomes redundant and the following is a fork
of `fastapi-users-db-sqlalchemy` using `asyncpg`.

Use this file until the official FastAPI-Users project supports this.
Discussion here https://github.com/fastapi-users/fastapi-users/discussions/717
"""

import uuid
from typing import Mapping, Optional, Type

from fastapi_users.db.base import BaseUserDatabase
from fastapi_users.models import UD
from pydantic import UUID4
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, func, select
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.types import CHAR, TypeDecorator

__version__ = "1.0.0"


class GUID(TypeDecorator):  # pragma: no cover
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise uses
    CHAR(36), storing as regular strings.
    """

    class UUIDChar(CHAR):
        python_type = UUID4

    impl = UUIDChar

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == "postgresql":
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return str(uuid.UUID(value))
            else:
                return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value


class SQLAlchemyBaseUserTable:
    """Base SQLAlchemy users table definition."""

    __tablename__ = "user"

    id = Column(GUID, primary_key=True)
    email = Column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password = Column(String(length=72), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)


class SQLAlchemyBaseOAuthAccountTable:
    """Base SQLAlchemy OAuth account table definition."""

    __tablename__ = "oauth_account"

    id = Column(GUID, primary_key=True)
    oauth_name = Column(String(length=100), index=True, nullable=False)
    access_token = Column(String(length=1024), nullable=False)
    expires_at = Column(Integer, nullable=True)
    refresh_token = Column(String(length=1024), nullable=True)
    account_id = Column(String(length=320), index=True, nullable=False)
    account_email = Column(String(length=320), nullable=False)

    @declared_attr
    def user_id(cls):
        return Column(GUID, ForeignKey("user.id", ondelete="cascade"), nullable=False)


class NotSetOAuthAccountTableError(Exception):
    """
    OAuth table was not set in DB adapter but was needed.
    Raised when trying to create/update a user with OAuth accounts set
    but no table were specified in the DB adapter.
    """

    pass


class SQLAlchemyUserDatabase(BaseUserDatabase[UD]):
    """
    Database adapter for SQLAlchemy.
    :param user_db_model: Pydantic model of a DB representation of a user.
    :param database: `Database` instance from `encode/databases`.
    :param users: SQLAlchemy users table instance.
    :param oauth_accounts: Optional SQLAlchemy OAuth accounts table instance.
    """

    users: Table
    oauth_accounts: Optional[Table]
    session: sessionmaker

    def __init__(
        self,
        user_db_model: Type[UD],
        session: sessionmaker,
        users: Table,
        oauth_accounts: Optional[Table] = None,
    ):
        super().__init__(user_db_model)
        self.session = session
        self.users = users
        self.oauth_accounts = oauth_accounts

    async def get(self, id: UUID4) -> Optional[UD]:
        async with self.session.begin() as session:
            query = select(self.users).where(self.users.c.id == id)
            result = await session.execute(query)
            user = result.first()

        return await self._make_user(user) if user else None

    async def get_by_email(self, email: str) -> Optional[UD]:
        async with self.session.begin() as session:
            query = self.users.select().where(
                func.lower(self.users.c.email) == func.lower(email)
            )
            result = await session.execute(query)
            user = result.first()
            return await self._make_user(user) if user else None

    async def get_by_oauth_account(self, oauth: str, account_id: str) -> Optional[UD]:
        if self.oauth_accounts is not None:
            async with self.session.begin() as session:
                query = (
                    select([self.users])
                    .select_from(self.users.join(self.oauth_accounts))
                    .where(self.oauth_accounts.c.oauth_name == oauth)
                    .where(self.oauth_accounts.c.account_id == account_id)
                )
                result = await session.execute(query)
                user = result.first()
                return await self._make_user(user) if user else None
        raise NotSetOAuthAccountTableError()
    
    
    async def get_by_id(self, id: str) -> Optional[UD]:
        if self.oauth_accounts is not None:
            async with self.session.begin() as session:
                query = (
                    select([self.users]).select_from(self.users.join(self.oauth_accounts)).where(self.users.c.id == id)
                )
                result = await session.execute(query)
                user = result.first()
                return await self._make_user(user) if user else None

    async def create(self, user: UD) -> UD:
        user_dict = user.dict()
        oauth_accounts_values = None

        if "oauth_accounts" in user_dict:
            oauth_accounts_values = []

            oauth_accounts = user_dict.pop("oauth_accounts")
            for oauth_account in oauth_accounts:
                oauth_accounts_values.append({"user_id": user.id, **oauth_account})

        query = self.users.insert().values(**user_dict)
        async with self.session.begin() as session:
            await session.execute(query)

        if oauth_accounts_values is not None:
            if self.oauth_accounts is None:
                raise NotSetOAuthAccountTableError()
            query = self.oauth_accounts.insert()

            async with self.session.begin() as session:
                await session.execute(query, oauth_accounts_values)

        return user

    async def update(self, user: UD) -> UD:
        user_dict = user.dict()

        if "oauth_accounts" in user_dict:
            if self.oauth_accounts is None:
                raise NotSetOAuthAccountTableError()

            delete_query = self.oauth_accounts.delete().where(
                self.oauth_accounts.c.user_id == user.id
            )
            async with self.session.begin() as session:
                await session.execute(delete_query)

            oauth_accounts_values = []
            oauth_accounts = user_dict.pop("oauth_accounts")
            for oauth_account in oauth_accounts:
                oauth_accounts_values.append({"user_id": user.id, **oauth_account})

            insert_query = self.oauth_accounts.insert()
            async with self.session.begin() as session:
                await session.execute(insert_query, oauth_accounts_values)

        update_query = (
            self.users.update().where(self.users.c.id == user.id).values(user_dict)
        )
        async with self.session.begin() as session:
            await session.execute(update_query)
        return user

    async def delete(self, user: UD) -> None:
        query = self.users.delete().where(self.users.c.id == user.id)
        async with self.session.begin() as session:
            await session.execute(query)

    async def _make_user(self, user: Mapping) -> UD:
        user_dict = {**user}

        if self.oauth_accounts is not None:
            query = self.oauth_accounts.select().where(
                self.oauth_accounts.c.user_id == user["id"]
            )
            async with self.session.begin() as session:
                result = await session.execute(query)
                oauth_accounts = result.all()
            user_dict["oauth_accounts"] = [{**a} for a in oauth_accounts]

        return self.user_db_model(**user_dict)
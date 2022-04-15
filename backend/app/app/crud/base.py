import abc
from typing import Generic, List, Type, TypeVar
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

# from app.db.errors import DoesNotExist
from app.schemas.base import BaseSchema

IN_SCHEMA = TypeVar("IN_SCHEMA", bound=BaseSchema)
SCHEMA = TypeVar("SCHEMA", bound=BaseSchema)
TABLE = TypeVar("TABLE")

import loguru

logger = loguru.logger


class CRUDBase(Generic[TABLE, IN_SCHEMA, SCHEMA], metaclass=abc.ABCMeta):
    def __init__(self, db_session: AsyncSession, *args, **kwargs) -> None:
        self._db_session: AsyncSession = db_session

    @property
    @abc.abstractmethod
    def _table(self) -> Type[TABLE]:
        ...

    @property
    @abc.abstractmethod
    def _schema(self) -> Type[SCHEMA]:
        ...

    async def create(self, in_schema: IN_SCHEMA) -> SCHEMA:
        item = self._table(id=uuid4(), **in_schema.dict())
        self._db_session.add(item)
        await self._db_session.commit()
        return self._schema.from_orm(item)

    async def update(self, item_id: UUID, update_schema) -> SCHEMA:
        item = await self._get_one(item_id)
        for key, value in update_schema.dict(exclude_unset=True).items():
            setattr(item, key, value)
        self._db_session.add(item)
        await self._db_session.commit()
        return self._schema.from_orm(item)

    async def delete(self, item_id: UUID) -> SCHEMA:
        item = await self._get_one(item_id)
        await self._db_session.delete(item)
        await self._db_session.commit()
        return self._schema.from_orm(item)

    async def _get_one(self, item_id: UUID):
        query = select(self._table).filter(self._table.id == item_id)
        try:
            item = (await self._db_session.execute(query)).scalar_one()
        except NoResultFound:
            item = None
        return item

    async def get_by_id(self, item_id: UUID) -> SCHEMA:
        item = await self._get_one(item_id)
        if not item:
            raise Exception("make NotFound error")
            # raise DoesNotExist(
            #     f"{self._table.__name__}<id:{item_id}> does not exist"
            # )
        return self._schema.from_orm(item)

    async def get_multi(self) -> List[SCHEMA]:
        query = select(self._table)
        results = (await self._db_session.execute(query)).scalars()
        return (self._schema.from_orm(item) for item in results)

    async def remove(self, item_id: UUID) -> SCHEMA:
        logger.warning("Deprecate Waring: use `delete` method instead")
        item = await self._get_one(item_id)
        await self._db_session.delete(item)
        await self._db_session.commit()
        return self._schema.from_orm(item)


# from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

# from pydantic import BaseModel
# from sqlalchemy import update
# from sqlalchemy.orm import Session
# from fastapi_crudrouter.core.databases import pydantify_record

# from app.db.base_class import Base
# from app.db.session import database

# ModelType = TypeVar("ModelType", bound=Base)
# CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
# UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


# class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
#     def __init__(self, model: Type[ModelType]):
#         """
#         CRUD object with default methods to Create, Read, Update, Delete (CRUD).

#         **Parameters**

#         * `model`: A SQLAlchemy model class
#         * `schema`: A Pydantic model (schema) class
#         """
#         self.model = model

#     async def get(self, id: Any) -> Optional[ModelType]:
#         record = await database.fetch_one(self.model.select().where(self.model.c.id == id))
#         if record:
#             return pydantify_record(record)
#         return None

#     async def get_multi(
#         self, *, skip: int = 0, limit: int = 100
#     ) -> List[ModelType]:
#         return pydantify_record(await database.fetch_all(self.model.select().offset(skip).limit(limit)))

#     async def create(self, *, obj_in: CreateSchemaType):  # -> ModelType:
#         query = self.model.insert()
#         try:
#             rid = await database.execute(query=query, values=obj_in.dict())
#             return await self.get(rid)
#         except Exception as e:
#             # TODO raise 422 "key already exists"
#             raise

#     async def update(
#         self,
#         id: Any,
#         *,
#         obj_in: Union[UpdateSchemaType, Dict[str, Any]]
#     ) -> ModelType:
#         if isinstance(obj_in, dict):
#             update_data = obj_in
#         else:
#             update_data = obj_in.dict(exclude_unset=True, exclude={"id"})
#         query = self.model.update().where(self.model.c.id == id)
#         try:
#             await database.fetch_one(
#                 query=query, values=update_data
#             )
#             return await self.get(id)
#         except Exception as e:
#             # TODO raise NOT_FOUND
#             raise

#     async def remove(self, *, id: int) -> ModelType:
#         query = self.model.delete().where(self.model.c.id == id)
#         try:
#             row = await self.get(id)
#             await database.execute(query=query)
#             return row
#         except Exception as e:
#             # TODO raise NOT_FOUND
#             raise

# from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

# from pydantic import BaseModel
# from sqlalchemy import update
# from sqlalchemy.orm import Session
# from fastapi_crudrouter.core.databases import pydantify_record

# # from app.db.base_class import Base
# from app.db.session import database


from re import A
from typing import Any, Generic, List, Optional, Type, TypeVar

import ormar
from ormar.exceptions import NoMatch
# from pydantic import UUID4

ModelType = TypeVar("ModelType", bound=ormar.Model)
# CreateSchemaType = TypeVar("CreateSchemaType", bound=ormar.Model)
# UpdateSchemaType = TypeVar("UpdateSchemaType", bound=ormar.Model)


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def _get_one(self, **kwargs: Any) -> Optional[ModelType]:
        try:
            item = await self.model.objects.filter(**kwargs).get()
        except NoMatch:
            return None
        # TODO **item to model definition required ???
        return item

    async def _get_multi(self, skip: int = 0, limit: int = 20, **kwargs: Any) -> List[ModelType]:
        return await self.model.objects.filter(**kwargs).offset(skip).limit(limit).all()

    async def get(self, id: Any) -> Optional[ModelType]:
        return await self._get_one(id=id)

    async def get_multi(self, *, skip: int = 0, limit: int = 20) -> List[ModelType]:
        return await self._get_multi(skip, limit)

    async def create(self, **kwargs) -> ModelType:
        return await self.model(**kwargs).save()

    async def update(self):
        pass

    async def remove(self):
        pass

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

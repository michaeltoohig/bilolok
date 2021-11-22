from typing import Any, Generic, List, Optional, Type, TypeVar

import ormar
from ormar.exceptions import NoMatch

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

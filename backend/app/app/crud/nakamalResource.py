from typing import Type

from app.crud.base import CRUDBase
from app.models.nakamal import NakamalResource
from app.schemas.nakamal import NakamalResourceSchemaIn, NakamalResourceSchema


class CRUDNakamalResource(CRUDBase[NakamalResource, NakamalResourceSchemaIn, NakamalResourceSchema]):    
    @property
    def _in_schema(self) -> Type[NakamalResourceSchemaIn]:
        return NakamalResourceSchemaIn

    @property
    def _schema(self) -> Type[NakamalResourceSchema]:
        return NakamalResourceSchema

    @property
    def _table(self) -> Type[NakamalResource]:
        return NakamalResource

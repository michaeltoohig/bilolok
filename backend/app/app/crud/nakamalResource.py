from typing import Type

from crud.base import CRUDBase
from models.nakamal import NakamalResource
from schemas.nakamal import NakamalResourceSchema, NakamalResourceSchemaIn


class CRUDNakamalResource(
    CRUDBase[NakamalResource, NakamalResourceSchemaIn, NakamalResourceSchema]
):
    @property
    def _in_schema(self) -> Type[NakamalResourceSchemaIn]:
        return NakamalResourceSchemaIn

    @property
    def _schema(self) -> Type[NakamalResourceSchema]:
        return NakamalResourceSchema

    @property
    def _table(self) -> Type[NakamalResource]:
        return NakamalResource

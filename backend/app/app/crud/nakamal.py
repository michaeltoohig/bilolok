from typing import Any, List, Optional, Type

from app.crud.base import CRUDBase
from app.models.nakamal import Nakamal
from app.schemas.nakamal import NakamalSchemaIn, NakamalSchema


class CRUDNakamal(CRUDBase[Nakamal, NakamalSchemaIn, NakamalSchema]):    
    @property
    def _in_schema(self) -> Type[NakamalSchemaIn]:
        return NakamalSchemaIn

    @property
    def _schema(self) -> Type[NakamalSchema]:
        return NakamalSchema

    @property
    def _table(self) -> Type[Nakamal]:
        return Nakamal

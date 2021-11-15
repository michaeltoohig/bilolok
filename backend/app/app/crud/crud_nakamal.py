from typing import Any, List, Optional

from app.crud.base import CRUDBase
from app.crud.crud_image import image as crud_image
from app.models.nakamal import Nakamal, NakamalTable
from app.schemas.nakamal import NakamalCreate, NakamalUpdate


class CRUDNakamal(CRUDBase[Nakamal, NakamalCreate, NakamalUpdate]):
    async def get(self, id: Any) -> Optional[Nakamal]:
        nakamal = await super().get(id)
        if nakamal:
            # TODO cache
            nakamal.image = await crud_image.get_one_by_nakamal(nakamal.id)
        return nakamal

    async def get_multi(self, *, skip: int = 0, limit: int = 100) -> List[Nakamal]:
        nakamals = await super().get_multi(skip=skip, limit=limit)
        for nakamal in nakamals:
            # TODO cache
            nakamal.image = await crud_image.get_one_by_nakamal(nakamal.id)
        return nakamals


nakamal = CRUDNakamal(NakamalTable)

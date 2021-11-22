from typing import Any, List, Optional

from app import models
from app.crud.base import CRUDBase
# from app.crud.crud_image import image as crud_image
# from app.models.nakamal import Nakamal


class CRUDNakamal(CRUDBase[models.Nakamal]):
    async def get(self, id: Any) -> Optional[models.Nakamal]:
        item = await self._get_one(id=id)
        # if item:
        #     # TODO cache
        #     item.image = await crud_image.get_one_by_nakamal(item.id)
        return item

    async def get_multi(self, **kwargs) -> List[models.Nakamal]:
        items = await self.model.objects.filter(**kwargs).all()
        # for item in items:
        #     # TODO cache
        #     item.image = await crud_image.get_one_by_nakamal(item.id)
        return items


nakamal = CRUDNakamal(models.Nakamal)

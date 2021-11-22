from typing import Any, List, Dict, Optional
from pathlib import Path

from fastapi_crudrouter.core.databases import pydantify_record
from ormar.exceptions import NoMatch
from sqlalchemy import desc

from app import models
from app.core.config import settings
from app.core.image import img_crypto_url
from app.crud.base import CRUDBase
from app.db.session import database
# from app.models.image import Image
from app.schemas.image import ImageCreate, ImageDB, ImageUpdate


class CRUDImage(CRUDBase[models.Image]):    
    def save_file(self, sfp: Path, *, nakamal_id: str, file_id: str, filename: str):
        """Save the given file to it's storage path defined by `filepath`."""
        ffp = Path(settings.IMAGES_LOCAL_DIR) / models.Image.build_filepath(nakamal_id, file_id, filename)
        ffp.parent.mkdir(parents=True, exist_ok=True)
        sfp.replace(str(ffp))  # removes original and assumes both are on same filesystem

    # def make_src(self, image: Image, width: int, height: int, **kwargs) -> str:
    #     uri = img_crypto_url.generate(
    #         width=width,
    #         height=height,
    #         smart=True,
    #         image_url=str(Image.build_filepath(image.nakamal.id, image.file_id, image.filename)),
    #         **kwargs,
    #     )
    #     return "{}{}".format(settings.THUMBOR_SERVER, uri)

    # def make_one_src(self, image: ImageDB) -> Dict[Any, Any]:
    #     image.src = self.make_src(image, height=1080, width=1920, full_fit_in=True)
    #     image.msrc = self.make_src(image, height=32, width=32, full_fit_in=True)
    #     image.thumbnail = self.make_src(image, height=200, width=200)
    #     return image

    # def make_all_src(self, images: List[ImageDB]) -> List[Dict[Any, Any]]:
    #     for image in images:
    #         image = self.make_one_src(image)
    #     return images

    async def get(self, id: str) -> Optional[models.Image]:
        record = await database.fetch_one(self.model.select().where(self.model.c.id == id))
        if record:
            image = pydantify_record(record)
            # image = self.make_one_src(image)
            return image
        return None

    async def get_multi(self, *, skip: int = 0, limit: int = 100) -> List[models.Image]:
        items = await self._get_multi(skip, limit)
        # items = self.make_all_src(items)
        return items

    async def get_multi_by_nakamal(self, nakamal_id: str, *, skip: int = 0, limit: int = 100) -> List[models.Image]:
        items = await self._get_multi(skip, limit, nakamal=nakamal_id)
        # items = self.make_all_src(items)
        return items

    async def get_one_by_nakamal(self, nakamal_id: str) -> models.Image:
        try:
            item = await self.model.objects.filter(nakamal=nakamal_id).first()
            # item = self.make_one_src(item)
            return item
        except NoMatch:
            return None


image = CRUDImage(models.Image)

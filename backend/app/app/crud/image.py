from typing import List, Type
from pathlib import Path
from uuid import UUID

from sqlalchemy import desc, select

from app.core.config import settings
from app.core.image import img_crypto_url
from app.crud.base import CRUDBase
from app.models.image import Image
from app.schemas.image import ImageSchemaIn, ImageSchema, ImageSchemaOut


class CRUDImage(CRUDBase[Image, ImageSchemaIn, ImageSchema]):    
    @property
    def _in_schema(self) -> Type[ImageSchemaIn]:
        return ImageSchemaIn

    @property
    def _schema(self) -> Type[ImageSchema]:
        return ImageSchema

    @property
    def _table(self) -> Type[Image]:
        return Image

    async def get_by_id(self, item_id: UUID) -> ImageSchema:
        item = await self._db_session.get(self._table, item_id)
        if not item:
            raise Exception("make NotFound error")
            # raise DoesNotExist(
            #     f"{self._table.__name__}<id:{item_id}> does not exist"
            # )
        item = self.make_src_urls(item)
        return self._schema.from_orm(item)

    async def get_multi(self) -> List[ImageSchema]:
        stmt = select(self._table)
        items = await self._db_session.execute(stmt)
        items = [self.make_src_urls(item[0]) for item in items]
        return (self._schema.from_orm(item) for item in items)
    
    def save_file(self, sfp: Path, *, nakamal_id: str, file_id: str, filename: str):
        """Save the given file to it's storage path defined by `filepath`."""
        ffp = Path(settings.IMAGES_LOCAL_DIR) / Image.build_filepath(nakamal_id, file_id, filename)
        ffp.parent.mkdir(parents=True, exist_ok=True)
        sfp.replace(str(ffp))  # removes original and assumes both are on same filesystem

    def make_src_url(self, image: Image, width: int, height: int, **kwargs) -> str:
        uri = img_crypto_url.generate(
            width=width,
            height=height,
            smart=True,
            image_url=str(Image.build_filepath(image.nakamal_id, image.file_id, image.filename)),
            **kwargs,
        )
        return "{}{}".format(settings.THUMBOR_SERVER, uri)

    def make_src_urls(self, image: ImageSchema) -> ImageSchemaOut:
        image.src = self.make_src_url(image, height=1080, width=1920, full_fit_in=True)
        image.msrc = self.make_src_url(image, height=32, width=32, full_fit_in=True)
        image.thumbnail = self.make_src_url(image, height=200, width=200)
        return image

    async def get_multi_by_nakamal(self, nakamal_id: str, *, skip: int = 0, limit: int = 100) -> List[Image]:
        stmt = select(self._table).where(self._table.nakamal_id == nakamal_id)
        items = await self._db_session.execute(stmt)
        items = [self.make_src_urls(item[0]) for item in items]
        return (self._schema.from_orm(item) for item in items)
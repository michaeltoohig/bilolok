from typing import List
from pathlib import Path

from fastapi_crudrouter.core.databases import pydantify_record
from sqlalchemy import desc

from app.core.config import settings
from app.core.image import img_crypto_url
from app.crud.base import CRUDBase
from app.db.session import database
from app.models.image import Image, ImageTable
from app.schemas.image import ImageCreate, ImageUpdate


class CRUDImage(CRUDBase[Image, ImageCreate, ImageUpdate]):    
    def save_file(self, sfp: Path, *, nakamal_id: str, file_id: str, filename: str):
        """Save the given file to it's storage path defined by `filepath`."""
        ffp = Path(settings.IMAGES_LOCAL_DIR) / Image.build_filepath(nakamal_id, file_id, filename)
        ffp.parent.mkdir(parents=True, exist_ok=True)
        sfp.replace(str(ffp))  # removes original and assumes both are on same filesystem

    def make_src(self, image: Image, width: int = None, height: int = None) -> str:
        uri = img_crypto_url.generate(
            width=width,
            height=height,
            smart=True,
            image_url=str(Image.build_filepath(image.nakamal_id, image.file_id, image.filename)),
        )
        return "{}{}".format(settings.THUMBOR_SERVER, uri)

    async def get_multi_by_nakamal(self, nakamal_id: str, *, skip: int = 0, limit: int = 100) -> List[Image]:
        return pydantify_record(await database.fetch_all(self.model.select() \
            .where(self.model.c.nakamal_id == nakamal_id) \
            .order_by(desc(self.model.c.created_at)) \
            .offset(skip).limit(limit)))


image = CRUDImage(ImageTable)

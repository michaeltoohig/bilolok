from typing import Any, List, Dict, Optional
from pathlib import Path

from ormar.exceptions import NoMatch

from app import models
from app.core.config import settings
from app.crud.base import CRUDBase


class CRUDImage(CRUDBase[models.Image]):    
    def save_file(self, sfp: Path, *, nakamal_id: str, file_id: str, filename: str):
        """Save the given file to it's storage path defined by `filepath`."""
        ffp = Path(settings.IMAGES_LOCAL_DIR) / models.Image.build_filepath(nakamal_id, file_id, filename)
        ffp.parent.mkdir(parents=True, exist_ok=True)
        sfp.replace(str(ffp))  # removes original and assumes both are on same filesystem

    async def get_multi(self, *, skip: int = 0, limit: int = 100) -> List[models.Image]:
        items = await self._get_multi(skip, limit)
        return items

    async def get_multi_by_nakamal(self, nakamal_id: str, *, skip: int = 0, limit: int = 100) -> List[models.Image]:
        return await self._get_multi(skip, limit, nakamal=nakamal_id)

    async def get_one_by_nakamal(self, nakamal_id: str) -> models.Image:
        try:
            return await self.model.objects.filter(nakamal=nakamal_id).first()
        except NoMatch:
            return None


image = CRUDImage(models.Image)

from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Optional, Type
from uuid import uuid4, UUID
from db.errors import DoesNotExist
from models.nakamal import NakamalProfile

from sqlalchemy import desc, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload
from sqlalchemy_utc import utcnow

from core.config import settings
from core.image import img_crypto_url
from crud.base import CRUDBase
from models.image import Image
from schemas.image import ImageSchema, ImageSchemaIn


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

    async def _get_one(self, item_id: UUID):
        query = (
            select(self._table)
            .options(selectinload(self._table.nakamal))
            .where(self._table.id == item_id)
        )
        try:
            (item,) = (await self._db_session.execute(query)).one()
        except NoResultFound:
            item = None
        return item

    async def create(self, in_schema: ImageSchemaIn) -> ImageSchema:
        item = self._table(id=uuid4(), **in_schema.dict())
        self._db_session.add(item)
        await self._db_session.commit()
        return await self.get_by_id(item.id)

    def save_file(self, sfp: Path, *, nakamal_id: str, file_id: str, filename: str):
        """Save the given file to it's storage path defined by `filepath`."""
        ffp = Path(settings.DATA_LOCAL_DIR) / self._table.build_filepath(
            nakamal_id, file_id, filename
        )
        ffp.parent.mkdir(parents=True, exist_ok=True)
        sfp.replace(
            str(ffp)
        )  # removes original and assumes both are on same filesystem

    def make_src_url(self, image: Image, width: int, height: int, **kwargs) -> str:
        uri = img_crypto_url.generate(
            width=width,
            height=height,
            smart=True,
            image_url=str(
                Image.build_filepath(image.nakamal.id, image.file_id, image.filename)
            ),
            **kwargs,
        )
        return "{}{}".format(settings.THUMBOR_SERVER, uri)

    def make_src_urls(self, image: ImageSchema) -> ImageSchema:
        image.src = self.make_src_url(
            image,
            height=720,
            width=1280,
            full_fit_in=True,
            filters=[
                "watermark(/images/watermark.png,20,-20,20,30)",
            ],
        )
        image.msrc = self.make_src_url(image, height=32, width=32, full_fit_in=True)
        image.thumbnail = self.make_src_url(image, height=200, width=200)
        return image

    async def get_by_id(self, item_id: UUID) -> ImageSchema:
        item = await self._get_one(item_id)
        if not item:
            raise DoesNotExist(
                f"{self._table.__name__}<id:{item_id}> does not exist"
            )
        item = self.make_src_urls(item)
        return self._schema.from_orm(item)

    async def get_multi(self, *, skip: int = 0, limit: int = 100) -> List[ImageSchema]:
        query = (
            select(self._table)
            .options(selectinload(self._table.nakamal))
            .order_by(desc(self._table.created_at))
            .offset(skip)
            .limit(limit)
        )
        results = await self._db_session.execute(query)
        items = (self.make_src_urls(item) for item in results.scalars())
        return (self._schema.from_orm(item) for item in items)

    async def get_recent(self) -> List[ImageSchema]:
        threshold = datetime.now(tz=timezone.utc) - timedelta(
            hours=settings.RECENT_THRESHOLD_HOURS
        )
        query = (
            select(self._table)
            .where(self._table.created_at >= threshold)
            .options(selectinload(self._table.nakamal))
            .order_by(desc(self._table.created_at))
        )
        results = await self._db_session.execute(query)
        items = (self.make_src_urls(item) for item in results.scalars())
        return (self._schema.from_orm(item) for item in items)

    async def get_multi_by_nakamal(
        self, nakamal_id: UUID, *, skip: int = 0, limit: int = 100
    ) -> List[ImageSchema]:
        query = (
            select(self._table)
            .options(selectinload(self._table.nakamal))
            .order_by(desc(self._table.created_at))
            .where(self._table.nakamal_id == nakamal_id)
        )
        results = await self._db_session.execute(query)
        items = (self.make_src_urls(item) for item in results.scalars())
        return (self._schema.from_orm(item) for item in items)

    async def create_nakamal_profile(
        self, image: ImageSchema,
    ) -> None:
        query = (
            select(NakamalProfile)
            .where(NakamalProfile.image_id == image.id)
        )
        result = await self._db_session.execute(query)
        item = result.scalars().first()
        if not item:
            # create new profile picture
            item = NakamalProfile(id=uuid4(), image_id=image.id, nakamal_id=image.nakamal.id)
            self._db_session.add(item)
            await self._db_session.commit()
        else:
            # update `updated_at` field on profile picture
            setattr(item, "updated_at", utcnow())
            self._db_session.add(item)
            await self._db_session.commit()
        return None

    async def get_current_nakamal_profile(
        self, nakamal_id: UUID
    ) -> ImageSchema:
        query = (
            select(NakamalProfile)
            .where(NakamalProfile.nakamal_id == nakamal_id)
            .order_by(NakamalProfile.updated_at.desc())
            .limit(1)
        )
        result = await self._db_session.execute(query)
        item = result.scalars().first()
        if not item:
            return None
        item = await self.get_by_id(item.image_id)
        item = self.make_src_urls(item)
        return item

    async def remove_nakamal_profile(
        self, image_id: UUID,
    ) -> None:
        query = (
            select(NakamalProfile)
            .where(NakamalProfile.image_id == image_id)
        )
        try:
            (item,) = (await self._db_session.execute(query)).one()
        except NoResultFound:
            return None
        await self._db_session.delete(item)
        await self._db_session.commit()
        return None

    async def get_multi_by_user(
        self,
        user_id: UUID,
        *,
        skip: int = 0,
        limit: int = 100,
        nakamal_id: Optional[UUID] = None
    ) -> List[ImageSchema]:
        query = (
            select(self._table)
            .options(selectinload(self._table.nakamal))
            .where(self._table.user_id == user_id)
        )
        if nakamal_id:
            query = query.where(self._table.nakamal_id == nakamal_id)
        query = query.order_by(desc(self._table.created_at))
        results = await self._db_session.execute(query)
        items = (self.make_src_urls(item) for item in results.scalars())
        return (self._schema.from_orm(item) for item in items)

    async def remove(self, item_id: UUID) -> ImageSchema:
        item = await self._get_one(item_id)
        await self.remove_nakamal_profile(item.id)  # remove any references in NakammalProfile table
        await self._db_session.delete(item)
        await self._db_session.commit()
        item = self.make_src_urls(item)
        return self._schema.from_orm(item)

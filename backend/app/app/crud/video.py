from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Optional, Type
from uuid import uuid4, UUID
from app.db.errors import DoesNotExist

from sqlalchemy import desc, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.crud.base import CRUDBase
from app.models.video import Video
from app.schemas.video import VideoSchemaIn, VideoSchema, VideoSchemaUpdate


class CRUDVideo(CRUDBase[Video, VideoSchemaIn, VideoSchema]):
    @property
    def _in_schema(self) -> Type[VideoSchemaIn]:
        return VideoSchemaIn

    @property
    def _schema(self) -> Type[VideoSchema]:
        return VideoSchema

    @property
    def _table(self) -> Type[Video]:
        return Video

    def _original_filepath(self, video: VideoSchema) -> Path:
        filename = "original/{f_id}{ext}".format(f_id=video.file_id, ext=Path(video.filename).suffix)
        return self._table.build_filepath(
            user_id=video.user.id,
            file_id=video.file_id,
            filename=filename,
        )

    def _video_filepath(self, video: VideoSchema) -> Path:
        filename = f"{video.file_id}.webm"
        return self._table.build_filepath(
            user_id=video.user.id,
            file_id=video.file_id,
            filename=filename,
        )

    def _cover_filepath(self, video: VideoSchema) -> Path:
        filename = f"{video.file_id}.jpg"
        return self._table.build_filepath(
            user_id=video.user.id,
            file_id=video.file_id,
            filename=filename,
        )

    def _social_thumbnail_filepath(self, video: VideoSchema) -> Path:
        filename = "social_thumbnail.jpg"
        return self._table.build_filepath(
            user_id=video.user.id,
            file_id=video.file_id,
            filename=filename,
        )

    # def make_src_url(self, video: VideoSchema) -> str:
    #     filename = f"{video.file_id}.webm"
    #     uri = self._table.build_filepath(video.user_id, video.file_id, filename)
    #     return "{}{}".format(settings.VIDEO_SERVER, uri)

    # def make_cover_url(self, video: VideoSchema) -> str:
    #     filename = f"{video.file_id}.jpg"
    #     uri = self._table.build_filepath(video.user_id, video.file_id, filename)
    #     return "{}{}".format(settings.VIDEO_SERVER, uri)

    def make_src_urls(self, video: VideoSchema) -> VideoSchema:
        if settings.DEBUG:
            # use static files returned by fastapi
            video.src = "{}/{}".format(settings.SERVER_HOST, self._video_filepath(video))
            video.cover = "{}/{}".format(settings.SERVER_HOST, self._cover_filepath(video))
            video.social_thumbnail = "{}/{}".format(settings.SERVER_HOST, self._social_thumbnail_filepath(video))
        else:
            video.src = "{}/{}".format(settings.VIDEO_SERVER, self._video_filepath(video))
            video.cover = "{}/{}".format(settings.VIDEO_SERVER, self._cover_filepath(video))
            video.social_thumbnail = "{}/{}".format(settings.VIDEO_SERVER, self._social_thumbnail_filepath(video))
        return video

    async def _get_one(self, item_id: UUID):
        query = (
            select(self._table)
            .options(selectinload(self._table.user))
            .options(selectinload(self._table.nakamal))
            .where(self._table.id == item_id)
        )
        try:
            (item,) = (await self._db_session.execute(query)).one()
        except NoResultFound:
            item = None
        return item

    def save_file(self, sfp: Path, *, user_id: str, file_id: str, filename: str):
        """Save the given file to it's storage path defined by `filepath`."""
        new_filename = "original/{f_id}{ext}".format(f_id=file_id, ext=Path(filename).suffix)
        ffp = Path(settings.DATA_LOCAL_DIR) / self._table.build_filepath(
            user_id, file_id, new_filename
        )
        ffp.parent.mkdir(parents=True, exist_ok=True)
        sfp.replace(
            str(ffp)
        )  # removes original and assumes both are on same filesystem

    async def get_by_id(self, item_id: UUID) -> VideoSchema:
        item = await self._get_one(item_id)
        if not item:
            raise DoesNotExist(
                f"{self._table.__name__}<id:{item_id}> does not exist"
            )
        item = self.make_src_urls(item)
        return self._schema.from_orm(item)

    async def get_multi(self, *, skip: int = 0, limit: int = 100) -> List[VideoSchema]:
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

    async def get_recent(self) -> List[VideoSchema]:
        threshold = datetime.now(tz=timezone.utc) - timedelta(
            hours=settings.RECENT_THRESHOLD_HOURS
        )
        query = (
            select(self._table)
            .where(self._table.created_at >= threshold)
            .options(selectinload(self._table.nakamal))
            .options(selectinload(self._table.user))
            .order_by(desc(self._table.created_at))
        )
        results = await self._db_session.execute(query)
        items = (self.make_src_urls(item) for item in results.scalars())
        return (self._schema.from_orm(item) for item in items)

    async def get_multi_by_nakamal(
        self, nakamal_id: str, *, skip: int = 0, limit: int = 100
    ) -> List[VideoSchema]:
        query = (
            select(self._table)
            .options(selectinload(self._table.nakamal))
            .order_by(desc(self._table.created_at))
            .where(self._table.nakamal_id == nakamal_id)
        )
        results = await self._db_session.execute(query)
        items = (self.make_src_urls(item) for item in results.scalars())
        return (self._schema.from_orm(item) for item in items)

    async def get_multi_by_user(
        self,
        user_id: UUID,
        *,
        skip: int = 0,
        limit: int = 100,
        nakamal_id: Optional[UUID] = None
    ) -> List[VideoSchema]:
        query = (
            select(self._table)
            .options(selectinload(self._table.user))
            .options(selectinload(self._table.nakamal))
            .where(self._table.user_id == user_id)
        )
        if nakamal_id:
            query = query.where(self._table.nakamal_id == nakamal_id)
        query = query.order_by(desc(self._table.created_at))
        results = await self._db_session.execute(query)
        items = (self.make_src_urls(item) for item in results.scalars())
        return (self._schema.from_orm(item) for item in items)

    async def create(self, in_schema: VideoSchemaIn) -> VideoSchema:
        item = self._table(id=uuid4(), **in_schema.dict())
        self._db_session.add(item)
        await self._db_session.commit()
        item = await self._get_one(item.id)
        item = self.make_src_urls(item)
        return self._schema.from_orm(item)

    async def update(self, item_id: UUID, update_schema: VideoSchemaUpdate) -> VideoSchema:
        item = await self._get_one(item_id)
        for key, value in update_schema.dict(exclude_unset=True).items():
            setattr(item, key, value)
        self._db_session.add(item)
        await self._db_session.commit()
        item = await self._get_one(item.id)
        item = self.make_src_urls(item)
        return self._schema.from_orm(item)

    async def delete(self, item_id: UUID) -> VideoSchema:
        item = await self._get_one(item_id)
        await self._db_session.delete(item)
        await self._db_session.commit()
        item = self.make_src_urls(item)
        return self._schema.from_orm(item)
from typing import List, Type
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload, aliased

from crud.base import CRUDBase
from models.image import Image
from models.nakamal import Nakamal
from schemas.nakamal import NakamalSchema, NakamalSchemaIn


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

    # async def get_id(self, item_id: UUID):
    #     profileImage = aliased(Image, name="profile")
    #     profile_id = (
    #         select(profileImage.id)
    #         .filter(profileImage.nakamal_id == self._table.id)
    #         .limit(1)
    #         .correlate(self._table)
    #         .scalar_subquery()
    #     )
    #     query = (
    #         select(self._table, Image)
    #         .options(selectinload(self._table.resources))
    #         .outerjoin(Image, Image.id == profile_id)
    #         .where(self._table.id == item_id)
    #     )
    #     item = (await self._db_session.execute(query)).scalar_one()
    #     return item
        # query = (
        #     select(self._table)
        #     .options(selectinload(self._table.resources))
        #     .where(self._table.id == item_id)
        # )
        # LastPost = aliased(Post, name='last')
        # last_id = (
        #     session.query(LastPost.id)
        #     .filter(LastPost.author_id == Author.id)
        #     .order_by(LastPost.publish_date.desc())
        #     .order_by(LastPost.id.desc())
        #     .limit(1)
        #     .correlate(Author)
        #     .as_scalar()
        # )

        # query = (
        #     DBSession.query(Author, Post)
        #     .outerjoin(Post, Post.id == last_id)
        # )

    async def create(self, in_schema: NakamalSchemaIn) -> NakamalSchema:
        item_id = uuid4()
        item = self._table(id=item_id, **in_schema.dict())
        self._db_session.add(item)
        await self._db_session.commit()
        return await self.get_by_id(item_id)

    async def _get_one(self, item_id: UUID):
        query = (
            select(self._table)
            .options(selectinload(self._table.resources))
            .where(self._table.id == item_id)
        )
        try:
            item = (await self._db_session.execute(query)).scalar_one()
        except NoResultFound:
            item = None
        return item

    async def get_multi(self) -> List[NakamalSchema]:
        query = select(self._table).options(selectinload(self._table.resources))
        results = await self._db_session.execute(query)
        # XXX why is this a generator exactly?
        return (self._schema.from_orm(item) for item in results.scalars())

    async def add_resource(self, item_id: UUID, resource):
        nakamal = await self._get_one(item_id)
        nakamal.resources.append(resource)
        # await self._db_session.add(nakamal)
        await self._db_session.commit()

    async def remove_resource(self, item_id: UUID, resource):
        nakamal = await self._get_one(item_id)
        nakamal.resources.remove(resource)
        # await self._db_session.add(nakamal)
        await self._db_session.commit()

    async def get_chiefs(self) -> List[NakamalSchema]:
        """Return list of nakamals that currently have a chief"""
        query = (
            select(self._table)
            .options(selectinload(self._table.resources))
            .where(self._table.chief_id != None)
        )
        results = await self._db_session.execute(query)
        return (self._schema.from_orm(item) for item in results.scalars())

    async def get_multi_by_chief(self, chief_id: UUID):
        query = (
            select(self._table)
            .options(selectinload(self._table.resources))
            .where(self._table.chief_id == chief_id)
        )
        results = await self._db_session.execute(query)
        return (self._schema.from_orm(item) for item in results.scalars())

    async def update_chief(self, item_id: UUID, chief_id: UUID):
        # Updating the chief is not available to users but handled by the system.
        # So I felt creating a one-off update method for this use case was better
        #  than adding logic to the normal nakamal schema and prevent the chief
        #  from being modified by users.
        # I may go back on this in the future and this may be an anti-pattern
        nakamal = await self._get_one(item_id)
        setattr(nakamal, "chief_id", chief_id)
        self._db_session.add(nakamal)
        await self._db_session.commit()
        return self._schema.from_orm(nakamal)
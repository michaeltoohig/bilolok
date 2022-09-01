from enum import Enum
from app.models.image import Image

from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import select, and_, Column, Float, ForeignKey, Integer, String, Table, Enum as SQLAEnum
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship, declared_attr, relation

from app.db.base_class import Base
from app.db.mixins import TimeMixin

nakamal_resource_association = Table(
    "nakamal_resource_assocation",
    Base.metadata,
    Column("nakamal_id", GUID, ForeignKey("nakamal.id"), primary_key=True),
    Column("resource_id", GUID, ForeignKey("nakamal_resource.id"), primary_key=True),
)



class NakamalProfile(Base, TimeMixin):
    __tablename__ = "nakamal_profile"
    nakamal_id = Column(GUID, ForeignKey("nakamal.id"), nullable=False)
    image_id = Column(GUID, ForeignKey("image.id"), nullable=False)


class Nakamal(Base, TimeMixin):
    """SQLAlchemy nakamals table definition."""

    __tablename__ = "nakamal"
    __versioned__ = {}

    name = Column(String, nullable=False)
    aliases = Column(ARRAY(String), nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    light = Column(String)
    owner = Column(String)
    phone = Column(String)
    windows = Column(Integer, default=1)
    chief_id = Column(GUID, ForeignKey("user.id"), nullable=True)
    chief = relationship("User", lazy="joined")

    # NOTE debating as to return the thumbnail URL directly or the full ImageSchema object
    # profile_id = Column(GUID, ForeignKey("image.id"), nullable=True)
    # profile = relationship("Image", foreign_keys=profile_id, lazy="joined")

    kava_source_id = Column(GUID, ForeignKey("nakamal_kava_source.id"), nullable=False)
    kava_source = relationship("NakamalKavaSource", lazy="joined")
    resources = relationship(
        "NakamalResource", secondary=nakamal_resource_association, lazy="joined"
    )
    area_id = Column(GUID, ForeignKey("nakamal_area.id"), nullable=False)
    area = relationship("NakamalArea", lazy="joined")

    @declared_attr
    def __mapper_args__(cls):
        # for original source
        # https://stackoverflow.com/questions/73509673/sqlalchemy-1-4-table-query-that-includes-first-result-of-second-table?noredirect=1#comment129824735_73509673
        children = NakamalProfile.__table__
        image = Image.__table__
        most_recent_profile = (
            select(children.c.image_id)
            .where(children.c.nakamal_id == cls.id)
            .order_by(children.c.updated_at.desc())
            .limit(1)
            .correlate(cls.__table__)
            .scalar_subquery()
        )

        rel = relation(
            "Image",
            primaryjoin=and_(
                Image.id == most_recent_profile, Image.nakamal_id == cls.id
            ),
            uselist=False,
            viewonly=True,
        )
        return {'properties': {'latest_profile': rel}}


class NakamalResource(Base):
    """SQLAlchemy nakamal resource table definition.

    Where a resource is amenity or feature of the nakamal.
    Examples:
      - Nakamal has food for sale
      - Nakamal has alcohol for sale
      - Nakamal has private shelters for groups
    """

    __tablename__ = "nakamal_resource"

    name = Column(String, nullable=False)


class Province(Enum):
    UNDEFINED = "UNDEFINED"
    ANY = "ANY"
    TORBA = "TORBA"
    PENAMA = "PENAMA"
    SANMA = "SANMA"
    MALAMPA = "MALAMPA"
    SHEFA = "SHEFA"
    TAFEA = "TAFEA"


class NakamalKavaSource(Base):
    """SQLAlchemy nakamal kava source table definition."""

    __tablename__ = "nakamal_kava_source"

    # XXX for now allow users to manually add islands but restrict the province field with Enum
    #  down the road we can standardize the island field but I want to see some raw responses first
    island = Column(String)
    province = Column(SQLAEnum(Province), nullable=False)


class NakamalArea(Base):
    """SQLAlchemy nakamal area table definition."""

    __tablename__ = "nakamal_area"

    name = Column(String, unique=True, nullable=False)


# class KavaPrice(Base):
#     volume =
#     price =
#     nakamal_id =


# class NakamalMessage(Base):
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     body = Column(String, nullable=False)
#     created_at = Column(DateTime, nullable=False, default=datetime.now)
#     # Relationships
#     nakamal_id = Column(Integer, ForeignKey('nakamal.id'), nullable=False)
#     # user_id = Column(GUID, ForeignKey('user.id'), nullable=False)

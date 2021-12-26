from enum import Enum
from sqlalchemy import Column, String, Float, Integer, ForeignKey
from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import Table
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from app.db.base_class import Base


# class Province(Enum):
#     NOT_KNOWN = "NOT_KNOWN"
#     TORBA = "TORBA"
#     PENAMA = "PENAMA"
#     SANMA = "SANMA"
#     MALAMPA = "MALAMPA"
#     SHEFA = "SHEFA"
#     TAFEA = "TAFEA"


nakamal_resource_association = Table('nakamal_resource_assocation', Base.metadata,
    Column("nakamal_id", GUID, ForeignKey("nakamal.id"), primary_key=True),
    Column("resource_id", GUID, ForeignKey("nakamal_resource.id"), primary_key=True),
)


class Nakamal(Base):
    """SQLAlchemy nakamals table definition."""

    __tablename__ = "nakamal"

    name = Column(String, nullable=False)
    aliases = Column(ARRAY(String))
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    light = Column(String)
    owner = Column(String)
    phone = Column(String)
    windows = Column(Integer, default=1)
    # kava_source = Column(Integer, default=KavaSource.UNKNOWN)
    # checkins = relationship("Checkin", cascade="save-update, merge, delete")
    resources = relationship("NakamalResource", secondary=nakamal_resource_association, lazy="joined")
    area_id = Column(GUID, ForeignKey("nakamal_area.id"), nullable=False)
    area = relationship("NakamalArea", lazy="joined")


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


# class NakamalKavaSource(Base):
#     """SQLAlchemy nakamal kava source table definition."""

#     __tablename__ = "nakamal_kava_source"

#     name = Column(String, unique=True, nullable=False)
#     province = Column(String, nullable=False)


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
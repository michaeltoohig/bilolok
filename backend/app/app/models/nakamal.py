from sqlalchemy import Column, String, Float, Integer, ForeignKey
from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import Table
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from app.db.base_class import Base


# class KavaSource(Enum):
#     "UNKNOWN" = 0
#     "MIX" = 1
#     "TORBA" = 2
#     "PENAMA" = 3
#     "SANMA" = 4
#     "MALAPA" = 5
#     "SHEFA" = 6
#     "TAFEA" = 7


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
    resources = relationship("NakamalResource", secondary=nakamal_resource_association, lazy="joined")


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


# class NakamalAlias(Base):
#     """Nakamal alias table definition."""

#     __tablename__ = "nakamal_alias"

#     name = Column(String, nullable=False)
#     # Relationships
#     user_id = Column(GUID, ForeignKey("user.id"), nullable=False)
#     user = relationship("User", lazy="joined")
#     nakamal_id = Column(GUID, ForeignKey("nakamal.id"), nullable=False)
#     nakamal = relationship("Nakamal", lazy="joined")


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
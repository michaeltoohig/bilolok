from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import UUID

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


class Nakamal(Base):
    """SQLAlchemy nakamals table definition."""

    __tablename__ = "nakamal"

    name = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    light = Column(String)
    owner = Column(String)
    phone = Column(String)
    # windows = Column(Integer)
    # kava_source = Column(Integer, default=KavaSource.UNKNOWN)


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
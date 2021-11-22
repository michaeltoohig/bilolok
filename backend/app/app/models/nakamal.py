from typing import Any, Dict, Optional
import uuid

import ormar
from ormar import property_field

from app import models
from app.db.session import metadata, database

# class KavaSource(Enum):
#     "UNKNOWN" = 0
#     "MIX" = 1
#     "TORBA" = 2
#     "PENAMA" = 3
#     "SANMA" = 4
#     "MALAPA" = 5
#     "SHEFA" = 6
#     "TAFEA" = 7


# class Nakamal(ormar.Model):
#     class Meta:
#         tablename = "nakamal"
#         metadata = metadata
#         database = database

#     id: uuid.UUID = ormar.UUID(primary_key=True, default=uuid.uuid4, uuid_format="string")
#     name: str = ormar.Text(nullable=False)
#     lat: float = ormar.Float(nullable=False)
#     lng: float = ormar.Float(nullable=False)
#     light: str = ormar.Text()
#     owner: str = ormar.Text()
#     phone: str = ormar.Text()
    # windows = Column(Integer)
    # kava_source = Column(Integer, default=KavaSource.UNKNOWN)



    # @property_field
    # def image(self):
    #     return 


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
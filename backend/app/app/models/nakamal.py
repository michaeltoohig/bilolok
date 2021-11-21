import ormar
from pydantic import UUID4

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


class Nakamal(ormar.Model):
    class Meta:
        # tablename = "nakamals"
        metadata = metadata
        database = database

    id: UUID4 = ormar.UUID(primary_key=True, uuid_format="string")
    name = ormar.Text(nullable=False)
    lat = ormar.Float(nullable=False)
    lng = ormar.Float(nullable=False)
    light = ormar.Text()
    owner = ormar.Text()
    phone = ormar.Text()
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
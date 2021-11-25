import uuid

from sqlalchemy import Column
from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: uuid.UUID = Column(GUID, primary_key=True, default=uuid.uuid4)
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

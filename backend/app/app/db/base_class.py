import uuid

from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import Column
from sqlalchemy.ext.declarative import as_declarative, declared_attr
# Setup sqlalchemy-continuum
from sqlalchemy_continuum import make_versioned
from sqlalchemy_continuum.plugins import PropertyModTrackerPlugin

from app.db.plugins import FastAPIUsersPlugin

make_versioned(
    plugins=[
        PropertyModTrackerPlugin(),
        FastAPIUsersPlugin(),
    ],
    user_cls="User",
)


@as_declarative()
class Base:
    id: uuid.UUID = Column(GUID, primary_key=True, default=uuid.uuid4)
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

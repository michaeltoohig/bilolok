import databases
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

metadata = MetaData()
database = databases.Database(settings.SQLALCHEMY_DATABASE_URI)

# XXX is below requied now that we use Ormar ???
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    connect_args={"options": "-c timezone=utc"},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

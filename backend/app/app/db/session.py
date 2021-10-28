import databases
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


database = databases.Database(settings.SQLALCHEMY_DATABASE_URI)
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    connect_args={"options": "-c timezone=utc"},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

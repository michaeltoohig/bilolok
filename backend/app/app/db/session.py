import databases
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


database = databases.Database(settings.SQLALCHEMY_DATABASE_URI)


async_engine = create_async_engine(
    settings.ASYNC_SQLALCHEMY_DATABASE_URI,
    echo=settings.SQLALCHEMY_DATABASE_ECHO,
    # pool_pre_ping=True,
    # connect_args={"options": "-c timezone=utc"},
)
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


# XXX sync engine/session for pre-start scripts and probably other good uses but not sure I'm using atm
sync_engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=settings.SQLALCHEMY_DATABASE_ECHO,
    pool_pre_ping=True,
    connect_args={"options": "-c timezone=utc"},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

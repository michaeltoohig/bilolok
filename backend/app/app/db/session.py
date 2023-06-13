from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings

async_engine = create_async_engine(
    settings.ASYNC_SQLALCHEMY_DATABASE_URI,
    echo=settings.SQLALCHEMY_DATABASE_ECHO,
)
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


# NOTE sync engine/session for pre-start scripts and alembic
sync_engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=settings.SQLALCHEMY_DATABASE_ECHO,
    pool_pre_ping=True,
    connect_args={"options": "-c timezone=utc"},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)

from pathlib import Path
from uuid import UUID

from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy_utc import UtcDateTime

from core.config import settings
from db.base_class import Base
from db.mixins import TimeMixin


class Trip(Base, TimeMixin):
    """SQLAlchemy trips table definition."""

    __tablename__ = "trip"

    start_at = Column(UtcDateTime, nullable=False)
    end_at = Column(UtcDateTime, nullable=False)
    data = Column(JSONB, nullable=False)
    # Relationships
    user_id = Column(GUID, ForeignKey("user.id"), nullable=False)
    user = relationship("User", lazy="joined")
    nakamal_id = Column(GUID, ForeignKey("nakamal.id"), nullable=False)
    nakamal = relationship("Nakamal", lazy="joined")
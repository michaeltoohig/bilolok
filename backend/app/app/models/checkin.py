from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import Boolean, Column, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from db.base_class import Base
from db.mixins import TimeMixin


class Checkin(Base, TimeMixin):
    """SQLAlchemy check-in table definition."""

    __tablename__ = "checkin"

    private = Column(Boolean, nullable=False, default=False)
    message = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    # Relationships
    user_id = Column(GUID, ForeignKey("user.id"), nullable=False)
    user = relationship("User", lazy="joined")
    nakamal_id = Column(GUID, ForeignKey("nakamal.id"), nullable=False)
    nakamal = relationship("Nakamal", lazy="joined")

from sqlalchemy import Column, String, ForeignKey, Boolean, Float
from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.db.mixins import TimeMixin


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

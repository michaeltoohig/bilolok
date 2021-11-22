# from fastapi_users.db.sqlalchemy import GUID
# from sqlalchemy import Boolean, Column, String, ForeignKey, Float

# from app.db.base_class import Base
# from app.db.mixins import TimeMixin


# class Checkin(Base, TimeMixin):
#     """SQLAlchemy check-in table definition."""
    
#     __tablename__ = "checkin"

#     id = Column(GUID, primary_key=True, nullable=False)
#     private = Column(Boolean, nullable=False, default=False)
#     message = Column(String)
#     lat = Column(Float)
#     lng = Column(Float)
#     # Relationships
#     user_id = Column(GUID, ForeignKey("user.id"), nullable=False)
#     nakamal_id = Column(GUID, ForeignKey("nakamal.id"), nullable=False)


# CheckinTable = Checkin.__table__

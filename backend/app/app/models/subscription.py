from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import Column, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB

from db.base_class import Base
from db.mixins import TimeMixin


class Subscription(Base, TimeMixin):
    """SQLAlchemy push notification subscriptions table definition."""

    __tablename__ = "subscription"
    __table_args__ = (UniqueConstraint("device_id", "user_id"),)

    subscription_info = Column("data", JSONB, nullable=False)
    device_id = Column(String, nullable=False)
    user_agent = Column(String, nullable=False)
    # Relationships
    user_id = Column(GUID, ForeignKey("user.id"), nullable=False)

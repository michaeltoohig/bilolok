from enum import Enum
from unicodedata import name
from sqlalchemy import Column, String, Float, Integer, ForeignKey, Enum as SQLAEnum
from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import Table
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.db.mixins import TimeMixin


delivery_service_user_association = Table('delivery_service_user_association', Base.metadata,
    Column("delivery_service_id", GUID, ForeignKey("delivery_service.id"), primary_key=True),
    Column("user_id", GUID, ForeignKey("user.id"), primary_key=True),
)


class DeliveryService(Base, TimeMixin):
    """SQLAlchemy kava delivery services table definition."""

    __tablename__ = "delivery_service"
    __versioned__ = {}

    name = Column(String, nullable=False)
    phone = Column(ARRAY(String), nullable=False)
    order_window = Column(JSONB, nullable=False)
    # dict(
    #   0=[],
    #   1=[12,13,14,15,16,17],
    #   2=...
    # )
    nakamal_id = Column(GUID, ForeignKey("nakamal.id"), nullable=True)
    nakamal = relationship("Nakamal", lazy="joined")
    menu = relationship("DeliveryServiceMenuItem", lazy="joined")


class DeliveryServiceMenuItem(Base, TimeMixin):
    __tablename__ = "delivery_service_menu_item"
    
    item = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    delivery_service_id = Column(GUID, ForeignKey("delivery_service.id"), nullable=False)
    delivery_service = relationship("DeliveryService", lazy="joined")


class KavaOrder(Base, TimeMixin):
    __tablename__ = "kava_order"
    
    delivery_service_id = Column(GUID, ForeignKey("delivery_service.id"), nullable=False)
    delivery_service = relationship("DeliveryService", lazy="joined")
    user_id = Column(GUID, ForeignKey("user.id"), nullable=True)
    # pickup details
    name = Column(String)
    phone = Column(String)
    comment = Column(String)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)


class KavaOrderItem(Base, TimeMixin):
    __tablename__ = "kava_order_item"

    kava_order_id = Column(GUID, ForeignKey("kava_order.id"), nullable=False)
    kava_order = relationship("KavaOrder", lazy="joined")
    item = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False, default=1)


"""
TODO:
map of all orders of a delivery service
select which to go to and show map with arrow etc
"""
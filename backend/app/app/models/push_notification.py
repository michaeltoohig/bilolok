from enum import Enum

from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import Column
from sqlalchemy import Enum as SQLAEnum
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB

from db.base_class import Base
from db.mixins import TimeMixin


class PushNotificationStatus(Enum):
    PENDING = "PENDING"
    SENT = "SENT"
    ERROR = "ERROR"


class PushNotification(Base, TimeMixin):
    __tablename__ = "push_notification"

    data = Column("data", JSONB, nullable=False)
    device_id = Column(String, nullable=False)
    status = Column(
        SQLAEnum(PushNotificationStatus),
        nullable=False,
        default=PushNotificationStatus.PENDING,
    )
    error_data = Column(JSONB)
    # seen_at = Column(UtcDateTime)
    # clicked_at = Column(UtcDateTime)
    # Relationships
    user_id = Column(GUID, ForeignKey("user.id"), nullable=False)

    # def __init__(
    #     self,
    #     id: uuid.UUID,
    #     device_id: str,
    #     user_id: uuid.UUID,
    #     data: Dict[str, Any],
    #     status: PushNotificationStatus = PushNotificationStatus.PENDING,
    # ):
    #     self.id = id
    #     self._data = data
    #     self.device_id = device_id
    #     self.user_id = user_id
    #     self.status = status

    # @property
    # def data(self):
    #     """Return push notification data with extra attributes."""
    #     d = self._data
    #     import pdb; pdb.set_trace()

    #     d["id"] = str(self.id)
    #     return d

    # @data.setter
    # def data(self, d):
    #     self._data = d

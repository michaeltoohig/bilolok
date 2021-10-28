from sqlalchemy import Column
from sqlalchemy_utc import UtcDateTime, utcnow


class TimeMixin(object):
    created_at = Column(UtcDateTime, default=utcnow())
    updated_at = Column(UtcDateTime, onupdate=utcnow())
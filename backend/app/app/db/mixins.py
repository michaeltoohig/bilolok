from datetime import datetime

import ormar
from sqlalchemy import func
from sqlalchemy_utc import utcnow


class TimeMixin:
    created_at = ormar.DateTime(timezone=True, default=func.now())
    updated_at = ormar.DateTime(timezone=True, nullable=True, onupdate=func.now())
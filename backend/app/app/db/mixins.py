from datetime import datetime

import ormar
from sqlalchemy import func
# from sqlalchemy_utc import utcnow


class TimeMixin:
    created_at = ormar.DateTime(timezone=True, default=datetime.now)
    updated_at = ormar.DateTime(timezone=True, nullable=True, onupdate=datetime.now)

    # TODO - validators to check times are UTC
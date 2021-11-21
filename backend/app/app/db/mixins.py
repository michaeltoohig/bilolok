import ormar


class TimeMixin:
    created_at = ormar.DateTime(timezone=True, default="CURRENT_TIMESTAMP")
    updated_at = ormar.DateTime(timezone=True, onupdate="CURRENT_TIMESTAMP")
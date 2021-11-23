# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import BaseMeta  # noqa
from app.models import (
    User,
    Nakamal,
    Image,
    Checkin,
)  # noqa

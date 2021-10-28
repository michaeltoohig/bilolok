# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.image import Image  # noqa
from app.models.nakamal import Nakamal  # noqa
from app.models.user import User  # noqa
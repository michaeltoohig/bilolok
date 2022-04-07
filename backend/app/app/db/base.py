# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.checkin import Checkin  # noqa
from app.models.image import Image  # noqa
from app.models.nakamal import Nakamal, NakamalResource, NakamalArea  # noqa
from app.models.push_notification import PushNotification  # noqa
from app.models.subscription import Subscription  # noqa
from app.models.user import User  # noqa

# For sqlalchemy-continuum
import sqlalchemy
sqlalchemy.orm.configure_mappers()
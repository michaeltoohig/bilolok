# Import all the models, so that Base has them before being
# imported by Alembic
# For sqlalchemy-continuum
import sqlalchemy

from db.base_class import Base  # noqa
from models.checkin import Checkin  # noqa
from models.image import Image  # noqa
from models.nakamal import Nakamal, NakamalArea, NakamalResource  # noqa
from models.push_notification import PushNotification  # noqa
from models.subscription import Subscription  # noqa
from models.trip import Trip  # noqa
from models.video import Video  # noqa
from models.user import User  # noqa

sqlalchemy.orm.configure_mappers()

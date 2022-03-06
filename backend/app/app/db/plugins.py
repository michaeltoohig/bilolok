from starlette_context import context
from sqlalchemy_continuum.plugins import Plugin


def fetch_current_user_id():
    return context.data.get("user_id")


def fetch_remote_addr():
    return context.data.get("X-Forwarded-For")


class FastAPIUsersPlugin(Plugin):
    def transaction_args(self, uow, session):
        return {
            "user_id": fetch_current_user_id(),
            "remote_addr": fetch_remote_addr()
        }

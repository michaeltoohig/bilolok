from sqlalchemy_continuum.plugins import Plugin
from starlette_context import context

# NOTE: I allow `None` for worker process outside of the request context to be able to modify versioned tables
# perhaps better would be to have a different result based on ENV_VAR that would return a static value such as "system" ?

def fetch_current_user_id():
    # Return None if we are outside of request context.
    if not context.exists():
        return
    return context.data.get("user_id")


def fetch_remote_addr():
    # Return None if we are outside of request context.
    if not context.exists():
        return
    return context.data.get("X-Forwarded-For")


class FastAPIUsersPlugin(Plugin):
    def transaction_args(self, uow, session):
        return {"user_id": fetch_current_user_id(), "remote_addr": fetch_remote_addr()}

from core.users import fastapi_users

current_active_user = fastapi_users.current_user(active=True)
current_active_verified_user = fastapi_users.current_user(active=True, verified=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
optional_current_superuser = fastapi_users.current_user(
    optional=True, active=True, superuser=True
)

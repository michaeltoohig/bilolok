import json
from typing import Any, Dict, List, Optional, Union

from pydantic import (
    AnyHttpUrl,
    BaseSettings,
    EmailStr,
    HttpUrl,
    PostgresDsn,
    RedisDsn,
    validator,
)

def list_parse_fallback(v):
    try:
        return json.loads(v)
    except Exception as e:
        return v.split(",")

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str  # secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_HOST: AnyHttpUrl
    # BACKEND_CORS_ORIGINS is a comma-delimited list
    # e.g: "http://localhost:8080,http://localhost:8000"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str
    PROJECT_SLUG: str
    SENTRY_DSN: Optional[HttpUrl] = None

    @validator("SENTRY_DSN", pre=True)
    def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
        if len(v) == 0:
            return None
        return v

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    REDIS_SERVER: str
    REDIS_PORT: int = 6379

    REDIS_CELERY_BROKER_DB: int = 0

    CELERY_BROKER_URI: Optional[RedisDsn] = None

    @validator("CELERY_BROKER_URI", pre=True)
    def assemble_celery_connection(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v
        return RedisDsn.build(
            scheme="redis",
            host=values.get("REDIS_SERVER"),
            port=str(values.get("REDIS_PORT")),
            path=f"/{values.get('REDIS_CELERY_BROKER_DB')}",
        )

    MAIL_TLS: bool = True
    MAIL_SSL: bool = True
    MAIL_PORT: Optional[int] = None
    MAIL_SERVER: Optional[str] = None
    MAIL_USERNAME: Optional[str] = None
    MAIL_PASSWORD: Optional[str] = None
    MAIL_FROM: Optional[EmailStr] = None
    MAIL_FROM_NAME: Optional[str] = None
    MAIL_USE_CREDENTIALS: bool = False

    @validator("MAIL_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "./app/email-templates/build"
    EMAILS_ENABLED: bool = False

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("MAIL_HOST")
            and values.get("MAIL_PORT")
            and values.get("MAIL_FROM")
        )

    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str
    USERS_OPEN_REGISTRATION: bool = False

    # TODO replace with Thumbor or other
    THUMBOR_SERVER: str
    THUMBOR_SECURITY_KEY: str
    IMAGES_LOCAL_DIR: str = "_local_images"

    class Config:
        case_sensitive = True
        json_loads = list_parse_fallback


settings = Settings()

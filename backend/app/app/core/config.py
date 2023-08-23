import json
import logging
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urlparse

from pydantic import (AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn,
                      validator)


def list_parse_fallback(v):
    try:
        return json.loads(v)
    except Exception:
        return v.split(",")


class Settings(BaseSettings):
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 8  # 8 days
    SERVER_HOST: AnyHttpUrl
    FRONTEND_HOST: AnyHttpUrl

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
    SENTRY_HOST: Optional[str] = None
    SENTRY_PROJECT_IDS: Optional[List[int]] = None

    @validator("SENTRY_HOST", pre=True)
    def extract_sentry_host(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if values.get("SENTRY_DSN", False):
            if isinstance(v, str):
                return v
            return urlparse(values.get("SENTRY_DSN")).hostname
        return None

    @validator("SENTRY_PROJECT_IDS", pre=True)
    def extract_sentry_project_id(
        cls, v: Optional[List[int]], values: Dict[str, Any]
    ) -> Any:
        if values.get("SENTRY_DSN", False):
            if isinstance(v, list):
                return v
            return [int(urlparse(values.get("SENTRY_DSN")).path.strip("/"))]
        return None

    VAPID_PRIVATE_KEY: str
    VAPID_PUBLIC_KEY: str
    VAPID_MAILTO: EmailStr

    LOG_FILE_PATH: str = "."
    LOG_FILE_ROTATION: str = "monday at 12:00"
    LOG_FILE_RETENTION: Union[int, str] = 8
    LOG_FILE_COMPRESSION: str = "gz"
    LOG_FILE_LEVEL: str = logging.INFO

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    SQLALCHEMY_DATABASE_ECHO: bool = False

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

    @property
    def ASYNC_SQLALCHEMY_DATABASE_URI(self) -> Optional[str]:
        return (
            self.SQLALCHEMY_DATABASE_URI.replace(
                "postgresql://", "postgresql+asyncpg://"
            )
            if self.SQLALCHEMY_DATABASE_URI
            else self.SQLALCHEMY_DATABASE_URI
        )

    REDIS_SERVER: str
    REDIS_PORT: int = 6379

    # XXX not using celery; using arq so we can remove this soon
    # REDIS_CELERY_BROKER_DB: int = 0
    # CELERY_BROKER_URI: Optional[RedisDsn] = None

    # @validator("CELERY_BROKER_URI", pre=True)
    # def assemble_celery_connection(
    #     cls, v: Optional[str], values: Dict[str, Any]
    # ) -> Any:
    #     if isinstance(v, str):
    #         return v
    #     return RedisDsn.build(
    #         scheme="redis",
    #         host=values.get("REDIS_SERVER"),
    #         port=str(values.get("REDIS_PORT")),
    #         path=f"/{values.get('REDIS_CELERY_BROKER_DB')}",
    #     )

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

    # @validator("EMAILS_ENABLED", pre=True)
    # def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
    #     return bool(
    #         values.get("MAIL_HOST")
    #         and values.get("MAIL_PORT")
    #         and values.get("MAIL_FROM")
    #     )

    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str
    USERS_OPEN_REGISTRATION: bool = False

    DATA_LOCAL_DIR: str
    THUMBOR_SERVER: str
    THUMBOR_SECURITY_KEY: str
    VIDEO_SERVER: str

    RECENT_THRESHOLD_HOURS: int = 4

    FFMPEG_COMMAND: str = "ffmpeg"

    class Config:
        case_sensitive = True
        json_loads = list_parse_fallback


settings = Settings()

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

from core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_TLS=settings.MAIL_TLS,
    MAIL_SSL=settings.MAIL_SSL,
    USE_CREDENTIALS=settings.MAIL_USE_CREDENTIALS,
    # VALIDATE_CERTS=True,
)


mail = FastMail(conf)

### Use:
# message = MessageSchema(...)
# await mail.send_message(message)
#

import json
from typing import Any
from app.crud.push_notification import CRUDPushNotification
from app.models.push_notification import PushNotificationStatus
from app.schemas.push_notification import PushNotificationSchemaIn, PushNotificationSchemaUpdate

from fastapi import APIRouter, Depends, status
from pydantic.networks import EmailStr
from sqlalchemy.ext.asyncio.session import AsyncSession
from pywebpush import webpush, WebPushException

from app.api.deps.user import current_superuser
from app.core.arq_app import get_arq_app
from app.core.config import settings
from app.api.deps.db import get_db
from app.crud.subscription import CRUDSubscription
from app.core.mail import mail, MessageSchema

router = APIRouter()


# @router.post(
#     "/test-arq", status_code=status.HTTP_201_CREATED
# )
# async def test_arq(
#     msg: schemas.Msg,
#     superuser: models.User = Depends(current_superuser),
# ) -> Any:
#     """
#     Test Arq worker.
#     """
#     arq_app = await get_arq_app()
#     await arq_app.enqueue_job(
#         "test_arq", msg.msg,
#     )
#     return {"msg": "Word received"}


# @router.post(
#     "/test-arq/test-email", status_code=status.HTTP_201_CREATED
# )
# async def test_arq_test_email(
#     email_to: EmailStr,
#     superuser: models.User = Depends(current_superuser),
# ) -> Any:
#     """
#     Test emails.
#     """
#     arq_app = await get_arq_app()
#     await arq_app.enqueue_job(
#         "send_test_email", email_to,
#     )
#     return {"msg": "Test email sent"}

from app.models.user import User

@router.post(
    "/test-email", status_code=status.HTTP_201_CREATED,
)
async def test_email(
    email_to: EmailStr,
    superuser: User = Depends(current_superuser),
) -> Any:
    """
    Test emails.
    """
    message = MessageSchema(
        subject="Test Email",
        recipients=[email_to],
        body="This email is a test."
    )
    await mail.send_message(message)
    return {"msg": "Test email sent"}


@router.post(
    "/test-push-notification", status_code=status.HTTP_201_CREATED,
)
async def test_push_notification(
    db: AsyncSession = Depends(get_db),
    superuser: User = Depends(current_superuser),
) -> Any:
    """
    Test push notifications.
    """
    crud_pn = CRUDPushNotification(db)
    crud_subscription = CRUDSubscription(db)
    data = dict(body="Testing web push notification from Bilolok.")
    subs = await crud_subscription.find_multi_by_user_id(superuser.id)
    for sub in subs:
        push_notification = await crud_pn.create(PushNotificationSchemaIn(
            user_id=sub.user_id,
            device_id=sub.device_id,
            data=data,
        ))
        try:
            data = push_notification.data
            data["id"] = str(push_notification.id)
            webpush(
                subscription_info=sub.subscription_info,
                data=json.dumps(data),
                vapid_private_key=settings.VAPID_PRIVATE_KEY,
                vapid_claims={
                    "sub": f"mailto:{settings.VAPID_MAILTO}",
                },
            )
            await crud_pn.update(push_notification.id, PushNotificationSchemaUpdate(
                status=PushNotificationStatus.SENT,
            ))
        except WebPushException as exc:
            error_data = dict(exc=repr(exc))
            # Mozilla returns additional information in the body of the response.
            if exc.response and exc.response.json():
                extra = exc.response.json()
                error_data["code"] = extra.code
                error_data["errno"] = extra.errno
                error_data["message"] = extra.message
            await crud_pn.update(push_notification.id, PushNotificationSchemaUpdate(
                status=PushNotificationStatus.ERROR,
                error_data=error_data,
            ))
    return {"msg": "okay"}
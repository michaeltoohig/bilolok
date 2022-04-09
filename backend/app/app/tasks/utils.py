import json

from pywebpush import WebPushException, webpush

from app.core.config import settings
from app.crud.push_notification import CRUDPushNotification
from app.crud.subscription import CRUDSubscription
from app.models.push_notification import PushNotificationStatus
from app.schemas.push_notification import (PushNotificationSchemaIn,
                                           PushNotificationSchemaUpdate)


async def test_arq_subtask(ctx: dict, letter: str):
    return f"test sub task return {letter}"


async def test_arq(ctx: dict, word: str):
    arq_app = ctx["redis"]
    for i, letter in enumerate(word):
        await arq_app.enqueue_job("test_arq_subtask", letter, _defer_by=1)
    return f"test task return {word}"


async def send_daily_push_notification(ctx: dict):
    db = ctx["db"]
    crud_pn = CRUDPushNotification(db)
    crud_subscription = CRUDSubscription(db)
    data = dict(body="It's kava time; try finding a kava bar on Bilolok and check-in.")
    subs = await crud_subscription.get_multi()
    for sub in subs:
        push_notification = await crud_pn.create(
            PushNotificationSchemaIn(
                user_id=sub.user_id,
                device_id=sub.device_id,
                data=data,
            )
        )
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
            await crud_pn.update(
                push_notification.id,
                PushNotificationSchemaUpdate(
                    status=PushNotificationStatus.SENT,
                ),
            )
        except WebPushException as exc:
            error_data = dict(exc=repr(exc))
            # Mozilla returns additional information in the body of the response.
            if exc.response and exc.response.json():
                extra = exc.response.json()
                error_data["code"] = extra.code
                error_data["errno"] = extra.errno
                error_data["message"] = extra.message
            await crud_pn.update(
                push_notification.id,
                PushNotificationSchemaUpdate(
                    status=PushNotificationStatus.ERROR,
                    error_data=error_data,
                ),
            )

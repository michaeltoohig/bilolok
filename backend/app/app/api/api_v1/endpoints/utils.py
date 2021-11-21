from typing import Any

from fastapi import APIRouter, Depends, status
from pydantic.networks import EmailStr

from app.api.deps import current_superuser
from app.core.arq_app import get_arq_app
from app.core.mail import mail, MessageSchema
from app.models.user import User

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


@router.post(
    "/test-email", status_code=status.HTTP_201_CREATED
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

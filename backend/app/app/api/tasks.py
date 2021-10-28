# Possibly needed to rename as these are just background tasks that run
#  without the need for a worker. We will have tasks that run with a worker in the future.

from fastapi import Request

from app.core.config import settings
from app.core.mail import mail, MessageSchema
from app.schemas.user import UserDB


async def on_after_register(user: UserDB, request: Request):
    print(f"User {user.id} has registered.")
    message = MessageSchema(
        subject="Welcome to Bilolok!",
        recipients=[user.email],
        body="Thanks for joining! You can also join our Facebook group to give feedback and suggest improvements for Bilolok."
    )
    await mail.send_message(message)


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    print(f"User {user.id} has forgot their password. Reset token: {token}")


def after_verification_request(user: UserDB, token: str, request: Request):
    print(f"Verification requested for user {user.id}. Verification token: {token}")
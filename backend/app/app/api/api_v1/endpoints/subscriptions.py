from typing import Any

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio.session import AsyncSession

from api.deps.db import get_db
from api.deps.user import current_active_user
from core.config import settings
from crud.subscription import CRUDSubscription
from models.user import User
from schemas.subscription import (SubscriptionPublicKeySchemaOut,
                                      SubscriptionSchemaIn,
                                      SubscriptionSchemaOut)

router = APIRouter(prefix="/subscriptions")


@router.get("", response_model=SubscriptionPublicKeySchemaOut)
async def get_subscription_public_key(
    current_user: User = Depends(current_active_user),
) -> Any:
    """
    Get VAPID public key to create a subscription.
    """
    return SubscriptionPublicKeySchemaOut(public_key=settings.VAPID_PUBLIC_KEY)


@router.post(
    "",
    response_model=SubscriptionSchemaOut,
    status_code=status.HTTP_201_CREATED,
)
async def post_subscription(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_active_user),
    *,
    in_schema: SubscriptionSchemaIn,
) -> Any:
    """Create subscription for user"""
    crud_subscription = CRUDSubscription(db)
    sub = await crud_subscription.find_by_device_id(
        in_schema.device_id, user_id=user.id
    )
    if sub:
        sub = await crud_subscription.update(sub.id, update_schema=in_schema)
    else:
        sub = await crud_subscription.create(in_schema=in_schema, user_id=user.id)
    return sub


@router.delete("")
async def delete_subscription(
    db: AsyncSession = Depends(get_db),
    *,
    user: User = Depends(current_active_user),
    device_id: str = Query(None, alias="deviceId"),
) -> Any:
    crud_subscription = CRUDSubscription(db)
    if device_id:
        sub = await crud_subscription.find_by_device_id(device_id, user_id=user.id)
        if sub:
            await crud_subscription.delete(sub.id)
        return {"msg": "User subscription deleted"}
    else:
        subs = await crud_subscription.find_multi_by_user_id(user.id)
        for sub in subs:
            await crud_subscription.delete(sub.id)
        return {"msg": "All user subscriptions deleted"}

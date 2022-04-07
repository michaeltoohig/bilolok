import uuid
from typing import Any, Dict

from .base import BaseSchema


class SubscriptionSchemaBase(BaseSchema):
    user_agent: str
    device_id: str
    subscription_info: Dict[str, Any]


class SubscriptionSchemaIn(SubscriptionSchemaBase):
    pass


class SubscriptionSchema(SubscriptionSchemaBase):
    id: uuid.UUID
    user_id: uuid.UUID


class SubscriptionSchemaOut(SubscriptionSchema):
    pass


#
# Public Key Schema
#


class SubscriptionPublicKeySchemaOut(BaseSchema):
    public_key: str

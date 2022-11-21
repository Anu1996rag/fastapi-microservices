from enum import Enum

from pydantic import BaseModel


class CreateOrder(BaseModel):
    id: str
    quantity: int


class OrderStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    REFUNDED = "refunded"


class OrderRedisGroups(str, Enum):
    ORDERS = 'orders-group'


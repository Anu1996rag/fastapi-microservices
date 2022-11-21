from enum import Enum


class RedisKeys(str, Enum):
    REFUND_ORDER = 'refund_order'
    ORDER_COMPLETED = 'order_completed'

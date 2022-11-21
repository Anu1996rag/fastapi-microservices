import time

from database import redis
from orders.models import Orders
from orders.schemas import OrderRedisGroups, OrderStatus
from enums import RedisKeys
from logger import logger

try:
    redis.xgroup_create(RedisKeys.REFUND_ORDER, OrderRedisGroups.ORDERS)
except:
    logger.info('Group already exists!')

while True:
    try:
        results = redis.xreadgroup(OrderRedisGroups.ORDERS, RedisKeys.REFUND_ORDER,
                                   {RedisKeys.REFUND_ORDER: '>'}, None)

        if results:
            for result in results:
                obj = result[1][0][1]
                order = Orders.get(obj['pk'])
                order.status = OrderStatus.REFUNDED
                order.save()

    except Exception as e:
        logger.error(str(e))
    time.sleep(1)

import time

from database import redis
from inventory.models import Product
from enums import RedisKeys
from inventory.schemas import InventoryRedisGroups
from logger import logger


try:
    redis.xgroup_create(RedisKeys.ORDER_COMPLETED, InventoryRedisGroups.INVENTORY)
except:
    logger.info('Group already exists!')

while True:
    try:
        results = redis.xreadgroup(InventoryRedisGroups.INVENTORY,
                                   RedisKeys.ORDER_COMPLETED, {RedisKeys.ORDER_COMPLETED: '>'}, None)

        if results:
            for result in results:
                obj = result[1][0][1]
                try:
                    product = Product.get(obj['product_id'])
                    product.quantity = product.quantity - int(obj['quantity'])
                    product.save()
                except Exception as err:
                    logger.info(f"Exception while updating {str(err)}")
                    redis.xadd(RedisKeys.REFUND_ORDER, obj, '*')

    except Exception as e:
        logger.error(str(e))
    time.sleep(1)

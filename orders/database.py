from redis_om import get_redis_connection
from logger import logger
from config import settings

try:
    redis = get_redis_connection(
        host=settings.orders_database_hostname,
        port=settings.orders_database_port,
        decode_responses=True
    )
except Exception as err:
    logger.error(f"Unable to connect to database : {str(err)}")

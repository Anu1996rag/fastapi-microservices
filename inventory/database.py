from redis_om import get_redis_connection
from config import settings
from logger import logger

try:
    redis = get_redis_connection(
        host=settings.inventory_database_hostname,
        port=settings.inventory_database_port,
        decode_responses=True
    )
except Exception as err:
    logger.error(f"Unable to connect to database : {str(err)}")

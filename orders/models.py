from redis_om import HashModel
from .database import redis


class Orders(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str

    class Meta:
        database = redis

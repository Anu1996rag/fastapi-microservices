import time

import requests

from ..models import Orders
from ..schemas import CreateOrder, OrderStatus
from ..database import redis
from fastapi import status, HTTPException
from fastapi.background import BackgroundTasks
from enums import RedisKeys
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter
from logger import logger
from config import settings

router = InferringRouter()


@cbv(router)
class OrdersAPI:
    router.prefix = "/orders"
    router.tags = ["Orders"]

    def __init__(self):
        self.products_url = f"http://{settings.inventory_microservice_hostname}:" \
                            f"{settings.inventory_microservice_port}products/"

    def save_to_orders(self, request_payload, prod_details):
        try:
            order = Orders(
                product_id=request_payload.id,
                price=prod_details["price"],
                fee=0.2 * prod_details["price"],
                total=1.2 * prod_details["price"],
                quantity=request_payload.quantity,
                status=OrderStatus.PENDING
            )
            order.save()
            return order

        except Exception as error:
            logger.error(f"Error while saving into orders : {str(error)}")

    def get_order(self, pk):
        return Orders.get(pk)

    @router.post("/", status_code=status.HTTP_201_CREATED)
    async def create_order(self, req: CreateOrder, background_tasks: BackgroundTasks):
        try:
            response = requests.get(f"{self.products_url}/%s" % req.id)
            prod_details = response.json()
        except Exception as error:
            logger.error(f"Error while fetching product details with the id : {req.id} : {str(error)}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Requested product details are not found")

        order = self.save_to_orders(req, prod_details)

        if not order:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Requested product details cannot be saved. Retry after few seconds.")

        background_tasks.add_task(self.order_completed, order)

        return order

    @router.get("/{order_id}")
    async def get_order_details(self, order_id: str):
        try:
            order = self.get_order(pk=order_id)
            if not order:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Unable to fetch order details")
            redis.xadd(RedisKeys.REFUND_ORDER, order.dict(), '*')
            return order
        except Exception as error:
            logger.error(f"Error while fetching order details : {str(error)}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Unable to fetch order details")

    @router.get("/")
    async def get_all_orders(self):
        try:
            all_orders = list(map(self.get_order, Orders.all_pks()))
            if not all_orders:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="Unable to fetch order details")
            return all_orders
        except Exception as error:
            logger.error(f"Error while fetching order details : {str(error)}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Unable to fetch order details")

    def order_completed(self, order: Orders):
        time.sleep(5)
        try:
            order.status = OrderStatus.COMPLETED
            order.save()
            redis.xadd(RedisKeys.ORDER_COMPLETED, order.dict(), '*')
        except Exception as error:
            logger.error(str(error))

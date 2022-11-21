import pytest
from fastapi import status
from config import settings
from inventory.models import Product
from orders.schemas import CreateOrder


@pytest.fixture
def product():
    return Product(
        name="test",
        price=100.00,
        quantity=10
    )


@pytest.fixture
def order():
    return CreateOrder(
        id="01GJ5HD446S7104SBMY1JWCJF7",
        quantity=100
    )


@pytest.fixture
def inventory_url():
    return f'http://{settings.inventory_microservice_hostname}:{settings.inventory_microservice_port}/products'


@pytest.fixture
def orders_url():
    return f'http://{settings.orders_microservice_hostname}:{settings.orders_microservice_port}/orders'


class InMemoryInventory:
    def __init__(self):
        self.products = []

    def add_product(self, product: Product):
        product.id = "12345"
        self.products.append(product.dict())
        return status.HTTP_201_CREATED, product.dict()

    def delete_product(self, id):
        for product in self.products:
            if product.get(id) == id:
                self.products.remove(product)
                return status.HTTP_204_NO_CONTENT
        return status.HTTP_403_FORBIDDEN


@pytest.fixture
def inventory():
    return InMemoryInventory()


class InMemoryOrders:
    def __init__(self):
        self.orders = []

    def add_order(self, order: CreateOrder):
        self.orders.append(order.dict())
        return status.HTTP_201_CREATED


@pytest.fixture
def inventory():
    return InMemoryInventory()


@pytest.fixture
def orders():
    return InMemoryOrders()

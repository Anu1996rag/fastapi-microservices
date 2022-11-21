import pytest
import requests
from fastapi import status


@pytest.mark.parametrize("order_id", ["01GJCE4PV8P718J8BER17MW7CH"])
def test_get_order_details_success(order_id, orders_url):
    response = requests.get(f'{orders_url}/{order_id}')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("order_id", ["0erCJF7"])
def test_get_order_details_failure(order_id, orders_url):
    response = requests.get(f'{orders_url}/{order_id}')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_all_orders(orders_url):
    response = requests.get(orders_url)
    assert response.status_code == status.HTTP_200_OK


def test_create_order(orders, order):
    response = orders.add_order(order)
    assert response == status.HTTP_201_CREATED

import pytest
import requests
from fastapi import status


@pytest.mark.parametrize("prod_id", ["01GJ5HD446S7104SBMY1JWCJF7"])
def test_get_product_details_success(prod_id, inventory_url):
    response = requests.get(f'{inventory_url}/{prod_id}')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("prod_id", ["0erCJF7"])
def test_get_product_details_failure(prod_id, inventory_url):
    response = requests.get(f'{inventory_url}/{prod_id}')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_all_products(inventory_url):
    response = requests.get(inventory_url)
    assert response.status_code == status.HTTP_200_OK


def test_create_product(inventory_url, product):
    response = requests.post(
        inventory_url,
        data=product.json())
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == product.name


@pytest.mark.parametrize("prod_id", ["01GJ5HD446S7104SBMY1JWCJF7"])
def test_delete_product(inventory, prod_id):
    result = inventory.delete_product(prod_id)
    assert result == status.HTTP_403_FORBIDDEN

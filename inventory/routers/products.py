from ..models import Product
from fastapi import HTTPException, status
from fastapi_restful.cbv import cbv
from fastapi_restful.inferring_router import InferringRouter
from logger import logger

router = InferringRouter()


@cbv(router)
class ProductsAPI:
    router.prefix = "/products"
    router.tags = ["Products"]

    def get_single_product(self, pk: str):
        logger.info(f"Fetching product with id : {pk}")
        try:
            product = Product.get(pk)
            return product.dict()
        except Exception as error:
            logger.info(f"Unable to fetch product details : {str(error)}")

    @router.get("/{prod_id}")
    def get_product_details(self, prod_id: str):
        product_details = self.get_single_product(pk=prod_id)
        if not product_details:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Product details not found")
        return product_details

    @router.get("/")
    async def get_all_products(self):
        all_products = list(map(self.get_single_product, Product.all_pks()))
        if not all_products:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Product details not found")
        return all_products

    @router.post("/", status_code=status.HTTP_201_CREATED)
    async def create_product(self, product: Product):
        try:
            return product.save()
        except Exception as error:
            logger.error(f"Unable to save into database : {str(error)}")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Requested action could not be performed")

    @router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete_products(self, product_id):
        try:
            return Product.delete(product_id)
        except Exception as error:
            logger.error(f"Unable to delete from database : {str(error)}")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Requested action could not be performed")

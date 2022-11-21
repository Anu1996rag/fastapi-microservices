from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import products
from config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[f'http://{settings.inventory_microservice_hostname}:{settings.inventory_microservice_port}'],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(products.router)


@app.get("/")
def inventory_home():
    return {"message": "Hello from the inventory microservice !!!"}

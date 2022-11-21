from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import orders
from config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[f'http://{settings.orders_microservice_hostname}:{settings.orders_microservice_port}'],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(orders.router)


@app.get("/")
def orders_home():
    return {"message": "Hello from the orders microservice !!!"}

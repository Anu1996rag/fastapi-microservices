from pydantic import BaseSettings


class Settings(BaseSettings):
    inventory_microservice_hostname: str
    inventory_microservice_port: str
    inventory_database_hostname: str
    inventory_database_port: str
    orders_microservice_hostname: str
    orders_microservice_port: str
    orders_database_hostname: str
    orders_database_port: str

    class Config:
        env_file = ".env"


settings = Settings()

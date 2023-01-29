import os
from os.path import join, dirname
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# for front-end
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD")

redis = get_redis_connection(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=DATABASE_PASSWORD,
    decode_responses=True
)


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


@app.get("/products")
def all():
    return [format(pk) for pk in Product.all_pks()]


def format(pk: str):
    product = Product.get(pk)

    return {
        "id": product.pk,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity

    }


@app.post("/products")
def create(product: Product):
    return product.save()


@app.get("/products/{pk}")
def get(pk: str):
    return Product.get(pk)


@app.delete("/products/{pk}")
def delete(pk: str):
    return Product.delete(pk)

import os
from os.path import join, dirname
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import requests
import time

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

# it should be another database, but for simplicity.. it's the same
redis = get_redis_connection(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=DATABASE_PASSWORD,
    decode_responses=True
)


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  # pending, completed, refunded

    class Meta:
        database = redis


@app.get("/orders/{pk}")
def get(pk: str):
    return Order.get(pk)


@app.post("/orders")
async def create(request: Request, background_task: BackgroundTasks):  # id, quantity
    body = await request.json()

    print("body:::::", body)

    req = requests.get("http://localhost:8000/products/%s" % body["id"])
    product = req.json()

    order = Order(
        product_id=body["id"],
        price=product["price"],
        fee=0.2 * product["price"],
        total=1.2 * product["price"],
        quantity=body["quantity"],
        status="pending"
    )
    order.save()

    background_task.add_task(order_completed, order)

    order_completed(order)

    return order


def order_completed(order: Order):
    time.sleep(5)
    order.status = "completed"
    order.save()
    redis.xadd("order_completed", order.dict(), '*')

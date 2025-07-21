from fastapi import FastAPI
from shopify import get_fulfillments

app = FastAPI()

@app.get("/order/{order_id}/fulfillments")
async def read_fulfillments(order_id: str):
    data = get_fulfillments(order_id)
    return data

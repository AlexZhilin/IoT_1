from typing import Optional

from fastapi import FastAPI

app = FastAPI()
temps = []


@app.get("/")
def read_root():
    return temps


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.post("/webhook")
def webhook(item: dict):
    print(item)
    temps.append(item["uplink_message"]["decoded_payload"])
    return {"success": True}

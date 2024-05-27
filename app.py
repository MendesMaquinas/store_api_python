import string
import uuid

from flask import Flask, request
from flask_smorest import abort
from db import items, stores

app = Flask(__name__)


@app.get("/stores")
def get_stores():
    return list(stores.values())


@app.get("/stores/<string:store_id>")
def get_stores_by_id(store_id):
    try:
        store = stores[store_id]
        if store is not None:
            return store
    except KeyError:
        return abort(404, message="Store not found")


@app.post("/stores")
def create_store():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(400, message="Informe o nome da sua loja")

    for store in stores.values():
        if store["name"] == store_data["name"]:
            abort(400, message="Loja já cadastrada.")

    store_id = uuid.uuid4().hex
    new_store = {**store_data, "id": store_id}
    stores[store_id] = new_store
    return new_store, 201


@app.get("/items")
def get_items():
    return list(items.values())


@app.post("/items")
def create_items():
    item_data = request.get_json()
    if (
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(404, message="Body deve conter proce,store_id e name")
    for item in items.values():
        if (
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(400, message="Item já existe")

    if item_data["store_id"] not in stores:
        abort(400, message="Loja não encontrada")

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item

    return item, 201


@app.get("/items/<string:item_id>")
def get_item(item_id):
    try:
        item = items[item_id]
        if item is not None:
            return item
    except KeyError:
        return abort(404, message="Item not found")


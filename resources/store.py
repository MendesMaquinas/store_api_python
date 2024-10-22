import uuid

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores
from schemas import StoreSchema, StoreUpdateSchema
blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            return abort(404, message="Store not found")

    @blp.arguments(StoreUpdateSchema)
    def put(self, store_data, store_id):
        try:
            if store_id not in stores:
                abort(404, message="Registro nao encontrado.")

            store = stores[store_id]
            store |= store_data

            return store
        except KeyError:
            abort(404, message="Loja não encontrado.")

    def delete(self, store_id):
        try:
            if store_id not in stores:
                abort(404, message="Registro nao encontrado.")

            del stores[store_id]
            return {"message": "Success"}
        except KeyError:
            abort(404, message="Loja não encontrado.")


@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        return {"stores": list(stores.values())}

    @blp.arguments(StoreSchema)
    def post(self, store_data):
        if "name" not in store_data:
            abort(400, message="Informe o nome da sua loja")

        for store in stores.values():
            if store["name"] == store_data["name"]:
                abort(400, message="Loja já cadastrada.")

        store_id = uuid.uuid4().hex
        new_store = {**store_data, "id": store_id}
        stores[store_id] = new_store
        return new_store, 201

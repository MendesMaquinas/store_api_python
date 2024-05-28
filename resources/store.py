import uuid

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores

blp = Blueprint("Stores", "stores", description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self):
        try:
            return stores["store_id"]
        except KeyError:
            return abort(404, message="Store not found")

    def post(self):
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

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Success"}
        except KeyError:
            abort(404, message="Loja não encontrado.")

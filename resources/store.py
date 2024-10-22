import uuid

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema
blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            return abort(404, message="Store not found")

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
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
@blp.response(200, StoreSchema(many=True))
class StoreList(MethodView):
    def get(self):
        return stores.values()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        for store in stores.values():
            if store["name"] == store_data["name"]:
                abort(400, message="Loja já cadastrada.")

        store_id = uuid.uuid4().hex
        new_store = {**store_data, "id": store_id}
        stores[store_id] = new_store
        return new_store, 201

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required, get_jwt

blp = Blueprint("Items", "items", description="Operations on items")


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            item = ItemModel.query.get_or_404(item_id)
            return item
        except KeyError:
            abort(404, message="Item not found.")

    @jwt_required()
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Privilégio de administrador necessário")
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item Deleted"}

    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
            if item_data["store_id"]: item.store_id = item_data["store_id"]

        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()

        return item

    @blp.route("/item")
    class ItemList(MethodView):
        @jwt_required()
        @blp.response(200, ItemSchema(many=True))
        def get(self):
            return ItemModel.query.all()

        @jwt_required()
        @blp.arguments(ItemSchema)
        @blp.response(201, ItemSchema)
        def post(self, item_data):

            if ItemModel.query.filter(ItemModel.name == item_data["name"]).first():
                abort(400, message="Item já cadastrado")

            item = ItemModel(**item_data)

            try:
                db.session.add(item)
                db.session.commit()
            except SQLAlchemyError:
                abort(500, message="Erro ao criar item.")
            return item

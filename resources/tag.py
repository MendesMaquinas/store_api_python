from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, StoreModel, ItemModel
from schemas import TagSchema, TagItemSchema

blp = Blueprint("Tags", "tags", description="Operations on tags")


@blp.route("/store/<string:store_id>/tag")
class TagInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        print("aaaaa")
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data["name"]).first():
            abort(400, message="Já existe uma tag com esse nome para a loja com o id " + store_id)
        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

    @blp.route("/item/<string:item_id>/tag/<string:tag_id>")
    class LinkTagsToItem(MethodView):

        @blp.response(201, TagSchema)
        def post(self, item_id, tag_id):
            item = ItemModel.query.get_or_404(item_id)
            tag = TagModel.query.get_or_404(tag_id)

            item.tags.append(tag)

            try:
                db.session.add(item)
                db.session.commit()
            except SQLAlchemyError:
                abort(500, message="Erro ao inserir tag")

        @blp.response(200, TagItemSchema)
        def delete(self, item_id, tag_id):
            item = ItemModel.query.get_or_404(item_id)
            tag = TagModel.query.get_or_404(tag_id)

            item.tags.remove(tag)

            try:
                db.session.add(item)
                db.session.commit()
            except SQLAlchemyError:
                abort(500, message="Erro ao deletar tag")

            return {"message": "Item removido da tag", "item": item, "tag": tag}

    @blp.route("/tag/<string:tag_id>")
    class Tag(MethodView):
        @blp.response(200, TagSchema)
        def get(self, tag_id):
            print(tag_id)
            tag = TagModel.query.get_or_404(tag_id)
            return tag

        @blp.response(202, description="Deleta a tag se não tiver um item relacionado.", example={"message": "Tag deletada"})
        @blp.alt_response(404, description="Tag não encontrada")
        @blp.alt_response(400, description="Se a tag for associada a mais de um item. Nesse caso a tag não será deletada.")
        def delete(self, tag_id):
            tag = TagModel.query.get_or_404(tag_id)

            if not tag.items:
                db.session.delete(tag)
                db.session.commit()
                return {"message": "Tag deleted"}
            abort(400, message="Erro ao deletar tag")
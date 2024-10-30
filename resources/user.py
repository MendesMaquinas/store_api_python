from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import pbkdf2_sha256

from db import db
from models import UserModel
from schemas import UserSchema
from flask.views import MethodView

blp = Blueprint("Users", "users", description="Operations on users")


@blp.route("/user/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(500, message="Usuário já cadastrado.")

        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )

        print(user.password)

        db.session.add(user)
        db.session.commit()
        return {"message": "Usuário criado com sucesso!"}, 201


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User Deleted"}, 200


@blp.route("/user")
class FindUser(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        users = UserModel.query.all()
        return users

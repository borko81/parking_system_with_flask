from flask_restful import Resource
from werkzeug.exceptions import BadRequest
from werkzeug.security import check_password_hash, generate_password_hash

from db import db
from managers.auth import AuthManager
from models.users import UserModel
from schemas.response.user_response_schema import UserResponceSchema


class UserRegisterManager(Resource):
    @staticmethod
    def insert_new_name(data):
        schema = UserResponceSchema()
        username = data["name"]
        if UserModel.find_from_name(username) is None:
            data["password"] = generate_password_hash(data["password"])
            user = UserModel(**data)
            db.session.add(user)
            db.session.commit()
            return schema.dump(user)
        raise BadRequest("Invalid username {}".format(username))


class UserDetailManager(Resource):
    @staticmethod
    def get_user(_id):
        user = UserModel.find_from_id(_id)
        if user.first() is not None:
            return user
        raise BadRequest("Invalid id {}".format(_id))

    @staticmethod
    def edit_user(_id, data):
        user = UserDetailManager.get_user(_id)
        user.update(data)
        return user

    @staticmethod
    def delete_user(_id):
        user = UserDetailManager.get_user(_id)
        db.session.delete(user.first())
        return 204


class UserLoginManager(Resource):
    @staticmethod
    def login(data):
        user_info = UserModel.find_from_name(data["name"])
        if user_info and check_password_hash(user_info.password, data["password"]):
            return AuthManager.encode_token(user_info)
        raise BadRequest("Invalid credential")

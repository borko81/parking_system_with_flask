from flask_restful import Resource
from werkzeug.exceptions import BadRequest, NotFound
from werkzeug.security import check_password_hash, generate_password_hash

from db import db
from helpers.data_preparation import data_preparate_for_commit
from helpers.decorator import validate_schema
from helpers.loger_config import custom_logger
from managers.auth import AuthManager
from models.users import UserModel
from schemas.request.user_request_schema import UserRegisterSchema
from schemas.response.user_response_schema import UserResponceSchema
from services.amazon_ses_services import SeSEmail
import json


class UserRegisterManager(Resource):
    @staticmethod
    @validate_schema(UserRegisterSchema)
    def insert_new_name(data):
        schema = UserResponceSchema()
        if UserModel.find_from_name(data["name"]) is None:
            data["password"] = generate_password_hash(data["password"])
            user = UserModel(**data)
            data_preparate_for_commit(user)
            SeSEmail().send_email(f"User with name: {data['name']} was created")
            return schema.dump(user)
        custom_logger(
            "error",
            f"Function insert_new_name: Try to tegister with not unique name ({data['name']})",
        )
        raise BadRequest("Invalid data, try again")


class UserDetailManager(Resource):
    @staticmethod
    def get_all_users():
        users = UserModel.query.all()
        schema = UserResponceSchema()
        return schema.dump(users, many=True)

    @staticmethod
    def get_user(_id):
        user = UserModel.find_from_id(_id)
        if user.first() is not None:
            return user
        custom_logger("error", f"Function get_user: not found user with id {_id}")
        raise NotFound("Invalid id {}".format(_id))

    @staticmethod
    def edit_user(_id, data):
        """
        Check in data user input password, if true encrypt, else continue
        model use for put and patch option
        :param _id:
        :param data: json
        :return: json
        """
        user = UserDetailManager.get_user(_id)
        try:
            data["password"] = generate_password_hash(data["password"])
        except KeyError:
            pass
        user.update(data)
        return user

    @staticmethod
    def delete_user(_id):
        user = UserDetailManager.get_user(_id)
        db.session.delete(user.first())
        custom_logger("info", f"Function delete_user: delete user with id {_id}")
        return 204


class UserLoginManager(Resource):
    @staticmethod
    def login(data):
        user_info = UserModel.find_from_name(data["name"])
        if user_info and check_password_hash(user_info.password, data["password"]):
            return AuthManager.encode_token(user_info)
        raise BadRequest("Invalid credential")

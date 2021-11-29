from flask import request
from flask_restful import Resource

from helpers.decorator import validate_schema, permission_required
from managers.user_manager import (
    UserRegisterManager,
    UserDetailManager,
    UserLoginManager,
)
from schemas.request.user_login_schema import UserLoginSchema
from schemas.request.user_request_schema import UserRegisterSchema, UserEditSchema
from schemas.response.user_response_schema import UserResponceSchema

from models.enum import UserType
from managers.auth import auth



class UserRegisterRes(Resource):
    @validate_schema(UserRegisterSchema)
    def post(self):
        """
        usage: curl 127.0.0.1:5000/user/register -X POST -H "Content-Type:application/json" -d '{"name": "Name G Name", "password": "A123", "type":"admin"}'
        :return: json
        """
        data = request.get_json()
        return UserRegisterManager.insert_new_name(data)


class ReturnAllUsersRes(Resource):
    """
    usage: curl 127.0.0.1:5000/user/users
    """
    @auth.login_required
    @permission_required(UserType.admin)
    def get(self):
        return UserDetailManager.get_all_users()


class UserLoginRes(Resource):
    @validate_schema(UserLoginSchema)
    def post(self):
        """
        usage: curl 127.0.0.1:5000/login -X POST -H "Content-Type:application/json" -d '{"password":"A123", "name":"Name G Name"}'
        :return: json
        """
        data = request.get_json()
        token = UserLoginManager.login(data)
        return {"token": token}, 200


class UserControlRes(Resource):
    @auth.login_required
    @permission_required(UserType.admin)
    def get(self, _id):
        """
        usage: curl 127.0.0.1:5000/user/8
        :param _id: int
        :return: json
        """
        schema = UserResponceSchema()
        return schema.dump(UserDetailManager.get_user(_id).first())

    @validate_schema(UserEditSchema)
    def put(self, _id):
        """
        usage: curl 127.0.0.1:5000/user/8 -X PUT -H "Content-Type:application/json" -d '{"name": "Boris Second Last"}'
        :param _id: int
        :return: json
        """
        data = request.get_json()
        schema = UserResponceSchema()
        return schema.dump(UserDetailManager.edit_user(_id, data).first())

    @validate_schema(UserEditSchema)
    def patch(self, _id):
        """
        usage: curl 127.0.0.1:5000/user/8 -X PATCH -H "Content-Type:application/json" -d '{"name": "Boris Second Last"}'
        :param _id: int
        :return: json
        """
        data = request.get_json()
        schema = UserResponceSchema()
        return schema.dump(UserDetailManager.edit_user(_id, data).first())

    def delete(self, _id):
        """
        usage: curl 127.0.0.1:5000/user/8 -X DELETE
        :param _id: int
        :return: 204 when success, BadRequest when not found id
        """
        return UserDetailManager.delete_user(_id)

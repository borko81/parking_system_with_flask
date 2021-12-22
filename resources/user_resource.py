from flask import request
from flask_restful import Resource

from helpers.decorator import validate_schema, permission_required
from managers.auth import auth
from managers.user_manager import (
    UserRegisterManager,
    UserDetailManager,
    UserLoginManager,
)
from models.enum import UserType
from schemas.request.user_login_schema import UserLoginSchema
from schemas.request.user_request_schema import UserRegisterSchema, UserEditSchema
from schemas.response.user_response_schema import UserResponceSchema


class UserRegisterRes(Resource):
    @auth.login_required
    @permission_required(UserType.admin)
    @validate_schema(UserRegisterSchema)
    def post(self):
        """
        usage: curl 127.0.0.1:5000/user/register -X POST -H "Content-Type:application/json" -d '{"name": "Name G Name", "password": "A123", "type":"admin"}'
        :return: json
        """
        data = request.get_json()
        return UserRegisterManager.insert_new_name(data), 201


class ReturnAllUsersRes(Resource):
    """
    usage: curl 127.0.0.1:5000/users -H "Content-Type:application/json" -H "Authorization: Bearer{{token}}"
    """

    @auth.login_required
    @permission_required(UserType.admin)
    def get(self):
        """
        Return all users info, need authorizations
        ---
        tags:
        - users detail
        parameters:
        - name: Authorization
          in: header
        responses:
          200:
            description: Return users info
        """
        return UserDetailManager.get_all_users()


class UserLoginRes(Resource):
    @validate_schema(UserLoginSchema)
    def post(self):
        """
        Login system
        usage: curl 127.0.0.1:5000/login -X POST -H "Content-Type:application/json" -d \
        '{"password":"A123", "name":"Name G Name"}'
        :return: json data
        ---
        tags:
        - users login
        parameters:
        - name: name
          in: body
        responses:
          200:
            description: Return token and status 200 when successful login
        """
        data = request.get_json()
        token = UserLoginManager.login(data)
        return {"token": token}, 200


class UserControlRes(Resource):
    @auth.login_required
    @permission_required(UserType.admin)
    def get(self, _id):
        """
        From given id return user info with this id, when id not valid return NotFound
        ---
        tags:
        - users detail
        parameters:
        - name: Authorization
          in: header
        - name: _id
          in: path
        responses:
          200:
            description: Return users info
            examples:
              url: /user/10
          404:
            description: Not found that id
          401:
            description: Unauthorized

        """
        schema = UserResponceSchema()
        return schema.dump(UserDetailManager.get_user(_id).first())

    @validate_schema(UserEditSchema)
    @auth.login_required
    @permission_required(UserType.admin)
    def put(self, _id):
        """
        If found user with path input id, may use put method to change data
        ---
        tags:
        - users detail
        parameters:
        - name: Authorization
          in: header
        - name: _id
          in: path
        - name: name
          in: body
        responses:
          200:
            description: OK
            example:
              _id: 18
          404:
            description: Not found that id
          401:
            description: Unauthorized
        """
        data = request.get_json()
        schema = UserResponceSchema()
        return schema.dump(UserDetailManager.edit_user(_id, data).first())

    @auth.login_required
    @permission_required(UserType.admin)
    def patch(self, _id):
        """
        If found user with path input id, may use patch method to change something in data
        ---
        tags:
        - users detail
        parameters:
        - name: Authorization
          in: header
        - name: _id
          in: path
        - name: name
          in: body
        responses:
          200:
            description: OK
            example:
              _id: 18
          404:
            description: Not found that id
          401:
            description: Unauthorized
        """
        data = request.get_json()
        schema = UserResponceSchema()
        return schema.dump(UserDetailManager.edit_user(_id, data).first())

    @auth.login_required
    @permission_required(UserType.admin)
    def delete(self, _id):
        """
        Delete users when found that id
        ---
        tags:
        - users detail
        parameters:
        - name: Authorization
          in: header
        - name: _id
          in: path
        responses:
          204:
            description: Successfully deleted
          404:
            description: Not found that id
          401:
            description: Unauthorized
        """
        return UserDetailManager.delete_user(_id), 204

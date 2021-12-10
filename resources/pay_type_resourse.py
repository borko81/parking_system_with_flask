from flask import request
from flask_restful import Resource

from helpers.decorator import validate_schema, permission_required
from managers.auth import auth
from managers.pay_type_manager import PayTypeManager, PayTypeIDManager
from models.enum import UserType
from schemas.request.pay_type_request import PayTypeRequest
from schemas.response.pay_type_response_schema import PayTypeResponseSchema


class PayTypeResourse(Resource):
    @auth.login_required
    def get(self):
        return PayTypeManager.get_all()

    @validate_schema(PayTypeRequest)
    @auth.login_required
    @permission_required(UserType.admin)
    def post(self):
        data = request.get_json()
        return PayTypeManager.insert_new(data)


class PayTypeIdResourse(Resource):
    @auth.login_required
    def get(self, _id):
        data = PayTypeIDManager.get(_id)
        schema = PayTypeResponseSchema()
        return schema.dump(data.first())

    @auth.login_required
    @permission_required(UserType.admin)
    def delete(self, _id):
        return PayTypeIDManager.delete(_id)

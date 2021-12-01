from flask import request
from flask_restful import Resource

from helpers.decorator import validate_schema, permission_required
from managers.auth import auth
from managers.park_manager import ParkingManager
from managers.parking_detail_id_manager import ParkingDetailFromIdManager
from models import UserType
from schemas.parking_schemas import ParkEnterSchema, ParkResponseSchema
from schemas.request.park_request_schema import ParkRequestSchemaForEdit
from schemas.response.park_response_schema import ParkResponseSchema as park_res_schema


class ParkingRes(Resource):
    @auth.login_required
    def get(self):
        """
        Show all car in parking who is not payed yet
        usage: curl 127.0.0.1:5000/parking
        """
        return ParkingManager.show_car_in_park()

    @validate_schema(ParkEnterSchema)
    @auth.login_required
    def post(self):
        """Here is a too big black magic"""
        data = request.get_json()
        return ParkingManager.input_new_car_in_park(data)


class ParkingDetailInfoRes(Resource):
    @staticmethod
    def return_result_in_json_use_schema(result):
        schema = park_res_schema()
        return schema.dump(result.first())

    @auth.login_required
    @permission_required(UserType.admin)
    def get(self, _id):
        result = ParkingDetailFromIdManager.get_from_id(_id)
        return ParkingDetailInfoRes.return_result_in_json_use_schema(result)

    @validate_schema(ParkRequestSchemaForEdit)
    @auth.login_required
    def put(self, _id):
        data = request.get_json()
        result = ParkingDetailFromIdManager.edit_car_in_park(_id, data)
        return self.return_result_in_json_use_schema(result)

    @auth.login_required
    def delete(self, _id):
        return ParkingDetailFromIdManager.delete_car_in_park(_id)


class ParkingPayRes(Resource):
    def post(self):
        pass


class ParkingAlreadyPay(Resource):
    def get(self):
        pass

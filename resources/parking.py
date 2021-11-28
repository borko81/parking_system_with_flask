from flask import request
from flask_restful import Resource

from helpers.decorator import validate_schema
from managers.park_manager import ParkingManager
from schemas.parking_schemas import ParkEnterSchema


class ParkingRes(Resource):
    def get(self):
        """
        Show all car in parking who is not payed yet
        usage: curl 127.0.0.1:5000/parking
        """
        return ParkingManager.show_car_in_park()

    @validate_schema(ParkEnterSchema)
    def post(self):
        """Here is a too big black magic"""
        data = request.get_json()
        return ParkingManager.input_new_car_in_park(data)


class ParkingDetailInfoRes(Resource):
    """Only from admin"""

    def get(self, _id):
        pass

    def put(self, _id):
        pass

    def delete(self, _id):
        pass


class ParkingPayRes(Resource):
    def post(self):
        pass


class ParkingAlreadyPay(Resource):
    def get(self):
        pass

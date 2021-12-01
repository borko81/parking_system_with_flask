from flask_restful import Resource, reqparse

from helpers.decorator import permission_required
from managers.auth import auth
from managers.park_capacity_manager import ParkCapacityManager
from models import UserType


class ParkingCapacityRes(Resource):
    parser = reqparse.RequestParser()

    @staticmethod
    def get():
        """
        usage: curl 127.0.0.1:5000/parking/capacity
        :return: parking capacity
        """
        capacity = ParkCapacityManager.get_capacity()
        return capacity.capacity

    @auth.login_required
    @permission_required(UserType.admin)
    def post(self):
        self.parser.add_argument("capacity", help="Capacity is required", required=True)
        args = self.parser.parse_args()
        try:
            capacity = args["capacity"]
            return ParkCapacityManager.insert_capacity(capacity)
        except KeyError:
            return {"error_message": "Not valid argument"}

    @auth.login_required
    @permission_required(UserType.admin)
    def put(self):
        self.parser.add_argument("capacity", help="Capacity is required", required=True)
        args = self.parser.parse_args()
        try:
            capacity = int(args["capacity"])
            return ParkCapacityManager.edit_capacity(capacity)
        except KeyError:
            return {"error_message": "Not valid argument"}

    @auth.login_required
    @permission_required(UserType.admin)
    def delete(self):
        return ParkCapacityManager.delete_row()

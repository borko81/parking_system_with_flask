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
        Return parking capacity
        ---
        tags:
        - Parking capacity
        responses:
          200:
            description: OK

        """
        capacity = ParkCapacityManager.get_capacity()
        return capacity.capacity

    @auth.login_required
    @permission_required(UserType.admin)
    def post(self):
        """
        Insert new capacity I get only first row, because that second insert is not needed
        ---
        tags:
        - Parking capacity
        parameters:
        - name: Authorization
          in: header
        - name: capacity
          in: body
        responses:
          201:
                description: Created
        """
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
        """
        Change capacity of parking, only work with frist row
        ---
        tags:
        - Parking capacity
        parameters:
        - name: Authorization
          in: header
        - name: capacity
          in: body
        responses:
          200:
                description: Success
        """
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
        """
        Delete row in model capacity
         ---
         tags:
         - Parking capacity
         parameters:
         - name: Authorization
           in: header
         responses:
           204:
                 description: Delete
        """
        return ParkCapacityManager.delete_row()

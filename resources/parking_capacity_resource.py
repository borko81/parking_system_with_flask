from flask_restful import Resource, reqparse

from managers.park_capacity_manager import ParkCapacityManager


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

    def post(self):
        """
        usage: curl 127.0.0.1:5000/parking/capacity -X POST -H "Content-Type:application/json" -d '{"capacity": 5}'
        :return:
        """

        self.parser.add_argument("capacity", help="Capacity is required", required=True)
        args = self.parser.parse_args()
        try:
            capacity = args["capacity"]
            return ParkCapacityManager.insert_capacity(capacity)
        except KeyError:
            return {"error_message": "Not valid argument"}

    def put(self):
        """
        usage: curl 127.0.0.1:5000/parking/capacity -X PUT -H "Content-Type:application/json" -d '{"capacity": 50}'
        :return: json message
        """
        self.parser.add_argument("capacity", help="Capacity is required", required=True)
        args = self.parser.parse_args()
        try:
            capacity = args["capacity"]
            return ParkCapacityManager.edit_capacity(capacity)
        except KeyError:
            return {"error_message": "Not valid argument"}

    def delete(self):
        """
        usage curl 127.0.0.1:5000/parking/capacity -X DELETE
        :return: status 204 when success
        """
        return ParkCapacityManager.delete_row()

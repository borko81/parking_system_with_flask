from werkzeug.exceptions import BadRequest

from db import db
from models.parking_capacity import ParkingCapacityModel


class ParkCapacityManager:
    @staticmethod
    def get_capacity():
        cap = ParkingCapacityModel.query.order_by("id").first()
        if cap:
            return cap.capacity
        raise BadRequest("Enter parking capacity")

    @staticmethod
    def insert_capacity(data):
        cap = ParkingCapacityModel(capacity=data)
        db.session.add(cap)
        db.session.flush()
        return {"message": "Success insert parking capacity"}, 201

    @staticmethod
    def edit_capacity(data):
        cap = ParkCapacityManager.get_capacity()
        cap.capacity = data
        return {"message": "Successfully change capacity"}

    @staticmethod
    def delete_row():
        cap = ParkCapacityManager.get_capacity()
        db.session.delete(cap)
        return 204

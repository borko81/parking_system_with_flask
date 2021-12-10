from werkzeug.exceptions import BadRequest

from db import db
from helpers.data_preparation import data_preparate_for_commit
from models.parking_capacity import ParkingCapacityModel


class ParkCapacityManager:
    @staticmethod
    def get_capacity():
        cap = ParkingCapacityModel.query.order_by("id").first()
        if cap:
            return cap
        raise BadRequest("Enter parking capacity")

    @staticmethod
    def insert_capacity(data):
        cap = ParkingCapacityModel(capacity=data)
        data_preparate_for_commit(cap)
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

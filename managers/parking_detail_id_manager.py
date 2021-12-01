from werkzeug.exceptions import NotFound, BadRequest

from db import db
from models.park import ParkModel


class ParkingDetailFromIdManager:
    @staticmethod
    def get_from_id(_id):
        check_id_exists = ParkModel.query.filter_by(id=_id)
        if check_id_exists.first():
            return check_id_exists
        raise NotFound("Not found this id {}".format(_id))

    @staticmethod
    def edit_car_in_park(_id, data):
        car: ParkModel = ParkingDetailFromIdManager.get_from_id(_id)
        if car.first().pay:
            raise BadRequest("Card is already payed, not allow editing!")
        car.update(data)
        return car

    @staticmethod
    def delete_car_in_park(_id):
        car: ParkModel = ParkingDetailFromIdManager.get_from_id(_id)
        if car.first().pay:
            raise BadRequest("Card is already payed, not allow editing!")
        db.session.delete(car.first())
        return 204

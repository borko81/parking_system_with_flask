import json
from datetime import datetime

from werkzeug.exceptions import BadRequest

from db import db
from models.park import ParkModel
from models.tarif_el import TarifPiceModel
from managers.park_capacity_manager import ParkCapacityManager
from schemas.parking_schemas import ParkResponseSchema
from models.subscription import SubscriptionModel


def validate_car_already_in_park(user_card):
    return ParkModel.query.filter_by(card=user_card).filter_by(outcome=None)


def conv_to_zerofill(param):
    return str(param).zfill(2)


def hours_and_minutes_from_seconds(sec):
    hours = int(sec // 3600)
    minutes = int((sec % 3600) // 60)
    return f"{conv_to_zerofill(hours)}:{conv_to_zerofill(minutes)}"


def calculate_total_time(time_enter, time_leave):
    total_time = (time_leave - time_enter).total_seconds()
    return hours_and_minutes_from_seconds(total_time)


def calculate_taxes_of_car(car):
    enter_time = car.first().income
    leave_time = datetime.now()
    total_time = calculate_total_time(enter_time, leave_time)
    price = TarifPiceModel.query.filter(TarifPiceModel.stay <= total_time)[-1]
    return price.price


def total_update_car_end_time_and_tax(car):
    price = calculate_taxes_of_car(car)
    car.update({"outcome": datetime.now(), "price": price})
    return float(price)


class ParkingManager:
    @staticmethod
    def show_car_in_park():
        schemas = ParkResponseSchema()
        return schemas.dump(ParkModel.query.filter_by(outcome=None), many=True)

    @staticmethod
    def get_free_space_in_park():
        return ParkCapacityManager.get_capacity() - len(ParkingManager.show_car_in_park())

    @staticmethod
    def input_new_car_in_park(data):
        test_car_already_in_park = validate_car_already_in_park(data["card"])
        free_space = ParkingManager.get_free_space_in_park()
        if test_car_already_in_park.first() is None and free_space > 0:
            car = ParkModel(**data)
            car.tarif_id = SubscriptionModel.get_from_card(data['card']).first().tar_type_id
            schema = ParkResponseSchema()
            db.session.add(car)
            db.session.flush()
            return schema.dump(car)
        elif free_space == 0:
            raise BadRequest("Not Enought space in park")
        price = total_update_car_end_time_and_tax(test_car_already_in_park)
        return {"message": "Car update successfully", "price": price}

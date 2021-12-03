from datetime import datetime

from werkzeug.exceptions import BadRequest, NotFound

from db import db
from helpers.data_preparation import data_preparate_for_commit
from models.park import ParkModel
from models.tarif_el import TarifPiceModel
from managers.park_capacity_manager import ParkCapacityManager
from schemas.parking_schemas import ParkResponseSchema
from models.subscription import SubscriptionModel

today = datetime.now()


def validate_car_already_in_park(user_card):
    """
    Check car already in park
    :param user_card: str
    """
    return ParkModel.query.filter_by(card=user_card).filter_by(outcome=None)


def conv_to_zerofill(param):
    """
    User to convert single int to double: 1 -> 01
    """
    return str(param).zfill(2)


def hours_and_minutes_from_seconds(sec):
    """
    Return total time for car stay in parking in seconds
    :param sec: int
    :return: string
    """
    hours = int(sec // 3600)
    minutes = int((sec % 3600) // 60)
    return f"{conv_to_zerofill(hours)}:{conv_to_zerofill(minutes)}"


def calculate_total_time(time_enter, time_leave):
    """
    Return time
    """
    total_time = (time_leave - time_enter).total_seconds()
    return hours_and_minutes_from_seconds(total_time)


def calculate_taxes_of_car(car):
    """
    After get stay time, check price for this. The price
    get from another model TarifPiceModel
    """
    enter_time = car.first().income
    leave_time = datetime.now()
    total_time = calculate_total_time(enter_time, leave_time)
    try:
        price = TarifPiceModel.query.filter(TarifPiceModel.stay <= total_time)[-1]
        return price.price
    except IndexError:
        raise BadRequest("This card stay less then 1 minute")


def total_update_car_end_time_and_tax(car):
    """
    If car is already in park and next opr is outcome, update parking
    outcome with price for stay time
    """
    price = calculate_taxes_of_car(car)
    car.update({"outcome": datetime.now(), "price": price})
    db.session.flush()
    return float(price)


class ParkingManager:
    @staticmethod
    def show_car_in_park():
        schemas = ParkResponseSchema()
        return schemas.dump(ParkModel.query.filter_by(outcome=None), many=True)

    @staticmethod
    def get_free_space_in_park():
        return ParkCapacityManager.get_capacity().capacity - len(
            ParkingManager.show_car_in_park()
        )

    @staticmethod
    def input_new_car_in_park(data):
        """
        If card not in park, insert it, otherwise, found card
        and update his param, add outcome time, price and so on.
        Calculate the time spent of a car at parking lot when the info
        by card or by id is retrieved.
        """
        card: SubscriptionModel = SubscriptionModel.get_from_card(data["card"]).first()

        if not card:
            raise NotFound("This card not found on server, try with another")
        elif card and card.active_date_to and card.active_date_to < today:
            raise BadRequest("This card is nо longer valid")

        if ParkingManager.get_free_space_in_park() == 0:
            raise BadRequest("Not Enough space in park")

        test_car_already_in_park = validate_car_already_in_park(data["card"])

        if not test_car_already_in_park.first():
            car = ParkModel(**data)
            car.tarif_id = card.tar_type_id
            schema = ParkResponseSchema()
            data_preparate_for_commit(car)
            return schema.dump(car)
        else:
            # TODO Think to delete card if stay is less then 1 minute
            id_for_stay = test_car_already_in_park.first().id
            price = total_update_car_end_time_and_tax(test_car_already_in_park)
            return {
                "message": "Found",
                "card": data["card"],
                "price": price,
                "id": id_for_stay,
            }

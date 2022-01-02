from abc import ABC, abstractmethod

from werkzeug.exceptions import BadRequest

from db import db
from helpers.loger_config import custom_logger
from managers.parking_detail_id_manager import ParkingDetailFromIdManager
from models.payment_transaction import Transaction
from services.wise import pay_with_wise


class BasePayManager(ABC):
    @staticmethod
    @abstractmethod
    def new_pay(_id):
        pass


def validate_already_payed_raise_error_else_return_what_needed(check_id):
    """Tracert park and check needed id is already is payed, if true not continue"""
    result = ParkingDetailFromIdManager.get_from_id(check_id)
    if result.first().pay:
        custom_logger(
            "error",
            f"Try to pay already payed card with id {check_id}",
        )
        raise BadRequest("This bill already is payed")
    if not result.first().price:
        custom_logger(
            "error",
            f"Try to pay card with id {check_id}, this card not have bill to pay",
        )
        raise BadRequest("This card not have bill yet")
    result = ParkingDetailFromIdManager.get_from_id(check_id)
    price = result.first().price
    return result, price


def update_and_return_message(result, price, _id, pay_type, trans_id=-2):
    """
    -2 hardcode for cash
    """
    data = {"pr_id": _id, "transaction_id": trans_id, "pay_type": pay_type}
    t = Transaction(**data)
    result.update({"pay": True})
    db.session.add(t)
    db.session.flush()
    return f"Success pay id: {_id}, sum: {price}."


class PayWiseManager(BasePayManager):
    """
    Pay with wise
    """

    @staticmethod
    def new_pay(_id: int):
        result, price = validate_already_payed_raise_error_else_return_what_needed(_id)
        trans_id = pay_with_wise(price)
        return update_and_return_message(result, price, _id, 2, trans_id)


class PayCashManager(BasePayManager):
    """
    Pay in cash
    """

    @staticmethod
    def new_pay(_id: int):
        result, price = validate_already_payed_raise_error_else_return_what_needed(_id)
        return update_and_return_message(result, price, _id, 1)

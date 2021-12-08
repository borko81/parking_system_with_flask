from decouple import config

from db import db
from helpers.striped_fields_in_model import StrippedString


class PayType(db.Model):
    __tablename__ = "pay_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        StrippedString(config("PAY_TYPE_LENGTH", cast=int)), nullable=False, unique=True
    )
    payment_name = db.relationship(
        "Transaction", backref="payment_name", lazy="dynamic"
    )

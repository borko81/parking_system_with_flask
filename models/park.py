from decouple import config
from datetime import datetime

from db import db


class ParkModel(db.Model):
    """
    Model save parking system
    TODO: too many query to get result!!!
    """

    __tablename__ = "park"

    id = db.Column(db.Integer, primary_key=True)
    card = db.Column(
        db.String(config("PARK_CARD_FIELDS_LENGTH", cast=int)),
        nullable=False,
        index=True,
    )
    tarif_id = db.Column(db.String(10), nullable=False)
    income = db.Column(db.DateTime, default=datetime.now())
    outcome = db.Column(db.DateTime, nullable=True, default=None)
    price = db.Column(db.Numeric(10, 2), nullable=True, default=None)
    pay = db.Column(db.Boolean, default=False)
    otc_id = db.Column(db.Integer, db.ForeignKey("otc.id"), nullable=True, default=None)

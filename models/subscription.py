from datetime import datetime

from db import db


class SubscriptionModel(db.Model):
    """
    Model save card number, reference to tarife type, is car valid or not
    """

    __tablename__ = "subscription"

    id = db.Column(db.Integer, primary_key=True)
    card = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(20), default="")
    email = db.Column(db.String(32), nullable=True)
    tar_type_id = db.Column(db.ForeignKey("tariftype.id"), nullable=False)
    active_date_from = db.Column(db.DateTime, nullable=False, default=datetime.now)
    active_date_to = db.Column(db.DateTime, nullable=True, default=None)

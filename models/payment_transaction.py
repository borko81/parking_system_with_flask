from sqlalchemy.sql import func

from db import db


class Transaction(db.Model):
    __tablename__ = "transaction"

    id = db.Column(db.Integer, primary_key=True)
    pr_id = db.Column(db.Integer, db.ForeignKey("park.id"), nullable=False)
    created_on = db.Column(db.DateTime, server_default=func.now())
    transaction_id = db.Column(db.Integer, nullable=False, default=None)
    pay_type = db.Column(db.Integer, db.ForeignKey("pay_type.id"), nullable=False)
    park_pay = db.relationship("ParkModel", backref="park_pay")

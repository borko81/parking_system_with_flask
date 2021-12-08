from db import db
from sqlalchemy.sql import func


class Transaction(db.Model):
    __tablename__ = "transaction"

    id = db.Column(db.Integer, primary_key=True)
    pr_id = db.Column(db.Integer, db.ForeignKey("park.id"), nullable=False)
    created_on = db.Column(db.DateTime, server_default=func.now())
    transaction_id = db.Column(db.Integer, nullable=False, default=None)
    pay_type = db.Column(db.Integer, db.ForeignKey("pay_type.id"), nullable=False)

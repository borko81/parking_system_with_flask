from typing import List

from sqlalchemy import func

from db import db


class OtcModel(db.Model):
    __tablename__ = "otc"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_model.id"), nullable=False)
    created_on = db.Column(db.DateTime, server_default=func.now())
    park_otc: List = db.relationship("ParkModel", backref="park_otc", lazy="dynamic")

from sqlalchemy import func

from db import db


class ParkingDocumentsModel(db.Model):
    __tablename__ = "documents"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    url = db.Column(db.String)
    create_on = db.Column(db.DateTime, server_default=func.now())

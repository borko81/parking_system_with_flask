from db import db


class OtcModel(db.Model):
    __tablename__ = "otc"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_model.id"), nullable=False)
    park_otc = db.relationship("ParkModel", backref="park_otc", lazy="dynamic")

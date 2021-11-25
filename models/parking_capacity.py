from db import db


class ParkingCapacityModel(db.Model):
    """
    Model save total capacity for parking, allow user change value
    """

    __tablename__ = "capacity"
    id = db.Column(db.Integer, primary_key=True)
    capacity = db.Column(db.Integer, nullable=False, default=10)

    def __repr__(self) -> str:
        return str(self.capacity)

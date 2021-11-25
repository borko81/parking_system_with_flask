from db import db
from models.enum import UserType


class UserModel(db.Model):
    """
    Model save user privilegs and validate data.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    type = db.Column(
        db.Enum(UserType),
        default=UserType.staff,
        nullable=False
    )
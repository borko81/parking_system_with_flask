from decouple import config
from sqlalchemy import func

from db import db
from models.enum import UserType


class UserModel(db.Model):
    """
    Model save user privileg, use two more cls method to optimize searches.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(config("USER_NAME_FIELD_LENGTH", cast=int)),
        nullable=False,
        unique=True,
    )
    password = db.Column(
        db.String(config("USER_PASSWORD_FIELD_LENGTH", cast=int)), nullable=False
    )
    type = db.Column(db.Enum(UserType), default=UserType.staff, nullable=False)
    create_on = db.Column(db.DateTime, server_default=func.now())

    @classmethod
    def find_from_name(cls, user_name):
        return cls.query.filter_by(name=user_name).first()

    @classmethod
    def find_from_id(cls, _id):
        return cls.query.filter_by(id=_id)

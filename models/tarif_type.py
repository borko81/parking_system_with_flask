from sqlalchemy import func

from db import db
from models.enum import TarifTypeEnum


class TariffTypeModel(db.Model):
    """
    Model save tarif plan, use enumerator
    TODO: think to remove enum, for ability to change and add names
    """

    __tablename__ = "tariftype"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.Enum(TarifTypeEnum),
        default=TarifTypeEnum.common,
        nullable=False,
        unique=True,
    )
    created_on = db.Column(db.DateTime, server_default=func.now())
    subscription = db.relationship(
        "SubscriptionModel", backref="subscription", lazy="dynamic"
    )

    @classmethod
    def find_by_name(cls, input_name):
        return cls.query.filter_by(name=input_name)

    @classmethod
    def find_by_id(cls, input_id):
        return cls.query.filter_by(id=input_id)

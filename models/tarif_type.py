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
        db.Enum(TarifTypeEnum), default=TarifTypeEnum.common, nullable=False
    )

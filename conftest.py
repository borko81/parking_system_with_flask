import pytest
from models.tarif_type import TariffTypeModel
from models.tarif_el import TarifPiceModel
from db import db


class GenerateTarifeData:
    @staticmethod
    def generate_tarif_id():
        t =TariffTypeModel(name="common")
        db.session.add(t)
        db.session.commit()

    @staticmethod
    def generate_tarif_price():
        t = TarifPiceModel(tarif_id=1, stay="00:01", price=1)
        db.session.add(t)
        db.session.commit()

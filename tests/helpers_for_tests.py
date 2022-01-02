from db import db
from models import (
    TariffTypeModel,
    TarifPiceModel,
    SubscriptionModel,
    ParkingCapacityModel,
)


class GenerateTarifeData:
    """
    Generate all needed data for test
    """

    @staticmethod
    def generate_tarif_id():
        t = TariffTypeModel(name="common")
        db.session.add(t)
        db.session.commit()

    @staticmethod
    def generate_tarif_price():
        t = TarifPiceModel(tarif_id=1, stay="00:01", price=1)
        db.session.add(t)
        db.session.commit()

    @staticmethod
    def generate_subscriber():
        s = SubscriptionModel(card="A123", email="123@abv.bg", tar_type_id=1)
        db.session.add(s)
        db.session.commit()

    @staticmethod
    def generate_slot():
        s = ParkingCapacityModel(capacity=2)
        db.session.add(s)
        db.session.commit()

    @staticmethod
    def generate_all_needed_data():
        GenerateTarifeData.generate_slot()
        GenerateTarifeData.generate_tarif_id()
        GenerateTarifeData.generate_tarif_price()
        GenerateTarifeData.generate_subscriber()

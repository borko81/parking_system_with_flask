import pytest
from flask_testing import TestCase
from sqlalchemy.exc import IntegrityError, DataError

from config import create_app
from db import db
from models import TarifPiceModel, TariffTypeModel


class TestTariElModels(TestCase):
    def create_app(self):
        return create_app("config.TestingConfig")

    def setUp(self):
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(self.app)
        db.create_all()
        tarife_name = TariffTypeModel(name="common")
        db.session.add(tarife_name)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_new_name_when_all_is_ok_insert_to_db(self):
        tarife_price = TarifPiceModel(tarif_id=1, stay="00:01", price=1)
        db.session.add(tarife_price)
        db.session.commit()
        check = TarifPiceModel.query.filter_by(id=1).first()
        assert check.tarif_id == 1
        assert (
            str(TariffTypeModel.query.filter_by(id=check.tarif_id).first().name)
            == "Common"
        )

    def test_create_new_price_but_not_valid_field_should_raise_error(self):
        with pytest.raises(IntegrityError) as ex:
            tarife_price = TarifPiceModel(stay="00:01", price=1)
            db.session.add(tarife_price)
            db.session.commit()
        assert 'null value in column "tarif_id"' in str(ex)

    def test_create_new_price_but_not_valid_field_stay_is_null_should_raise_error(self):
        with pytest.raises(IntegrityError) as ex:
            tarife_price = TarifPiceModel(tarif_id=1, price=1)
            db.session.add(tarife_price)
            db.session.commit()
        assert 'null value in column "stay"' in str(ex)

    def test_create_new_price_but_not_valid_field_price_is_null_should_raise_error(
        self,
    ):
        with pytest.raises(IntegrityError) as ex:
            tarife_price = TarifPiceModel(tarif_id=1, stay="00:01")
            db.session.add(tarife_price)
            db.session.commit()
        assert 'null value in column "price"' in str(ex)

    def test_create_new_price_len_of_price_not_valid_should_raise_error(self):
        with pytest.raises(DataError) as ex:
            tarife_price = TarifPiceModel(tarif_id=1, stay="00:01:00", price=1)
            db.session.add(tarife_price)
            db.session.commit()
        assert " value too long for type character" in str(ex)

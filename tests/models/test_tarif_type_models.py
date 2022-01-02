import pytest
from flask_testing import TestCase
from sqlalchemy.exc import DataError, IntegrityError

from config import create_app
from db import db
from models import TariffTypeModel


class TestTarifTypeModels(TestCase):
    def create_app(self):
        return create_app("config.TestingConfig")

    def setUp(self):
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_new_name(self):
        tarife_name = TariffTypeModel(name="vip")
        db.session.add(tarife_name)
        db.session.commit()
        validate_result = TariffTypeModel.query.filter_by(id=1)
        assert str(validate_result.first().name) == "Vip"

    def test_create_new_name_with_defaul_value(self):
        tarife_name = TariffTypeModel()
        db.session.add(tarife_name)
        db.session.commit()
        validate_result = TariffTypeModel.query.filter_by(id=1)
        assert str(validate_result.first().name) == "Common"

    def test_create_new_name_but_name_not_in_enum_should_raise_error(self):
        with pytest.raises(DataError) as ex:
            tarife_name = TariffTypeModel(name="unknown")
            db.session.add(tarife_name)
            db.session.commit()
        assert "invalid input value for enum tariftypeenum" in str(ex)

    def test_insert_duplicated_name_in_model(self):
        tarife_name = TariffTypeModel(name="common")
        db.session.add(tarife_name)
        db.session.commit()
        with pytest.raises(IntegrityError) as ex:
            tarife_name = TariffTypeModel(name="common")
            db.session.add(tarife_name)
            db.session.commit()
        assert "duplicate key value violates unique constraint" in str(ex)

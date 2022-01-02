import pytest
from flask_testing import TestCase
from sqlalchemy.exc import DataError, IntegrityError

from config import create_app
from db import db
from models import UserModel


class TestUserModels(TestCase):
    def create_app(self):
        return create_app("config.TestingConfig")

    def setUp(self):
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(self.app)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_happy_case_should_write_to_db(self):
        user = UserModel(name="First Second Last", password="A123", type="admin")
        db.session.add(user)
        db.session.commit()
        test_user = UserModel.query.filter_by(id=1).first()
        assert test_user.name == "First Second Last"
        assert test_user.password == "A123"

    def test_happy_case_with_default_type_should_write_to_db(self):
        user = UserModel(name="First Second Last", password="A123")
        db.session.add(user)
        db.session.commit()
        test_user = UserModel.query.filter_by(id=1).first()
        assert test_user.name == "First Second Last"
        assert str(test_user.type) == "Staff"

    def test_length_of_username_is_valid_when_not_should_raise_error(self):
        with pytest.raises(DataError) as ex:
            user = UserModel(name=f"First Second {'A' * 30}", password="A123")
            db.session.add(user)
            db.session.commit()
        assert "value too long for type character varying(32)" in str(ex)

    def test_unique_name_validation(self):
        user = UserModel(name="First Second Last", password="A123", type="admin")
        db.session.add(user)
        db.session.commit()

        # Test unique
        with pytest.raises(IntegrityError) as ex:
            user = UserModel(name="First Second Last", password="A123", type="admin")
            db.session.add(user)
            db.session.commit()
        assert (
            'duplicate key value violates unique constraint "user_model_name_key"'
            in str(ex)
        )

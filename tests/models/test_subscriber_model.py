import pytest
from flask_testing import TestCase
from sqlalchemy.exc import IntegrityError

from config import create_app
from db import db
from models import TariffTypeModel, SubscriptionModel


class TestUserModels(TestCase):
    def create_app(self):
        return create_app("config.TestingConfig")

    def setUp(self):
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(self.app)
        db.create_all()
        tar_type_id = TariffTypeModel(name="common")
        db.session.add(tar_type_id)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_happy_case_insert_new_subscriber(self):
        check = SubscriptionModel(
            card="A123",
            name="Some name",
            tar_type_id=1,
        )
        db.session.add(check)
        db.session.commit()
        assert len(SubscriptionModel.query.all()) == 1

    def test_insert_new_subscriber_but_with_wrong_type_should_raise_error(self):
        with pytest.raises(IntegrityError) as ex:
            check = SubscriptionModel(
                card="A123",
                name="Some name",
                tar_type_id=2,
            )
            db.session.add(check)
            db.session.commit()
        assert 'Key (tar_type_id)=(2) is not present in table "tariftype"' in str(ex)

    def test_insert_with_not_unique_card_should_raise_error(self):
        check = SubscriptionModel(
            card="A123",
            name="Some name",
            tar_type_id=1,
        )
        db.session.add(check)
        db.session.commit()
        with pytest.raises(IntegrityError) as ex:
            check = SubscriptionModel(
                card="A123",
                name="Some name",
                tar_type_id=1,
            )
            db.session.add(check)
            db.session.commit()
        assert "duplicate key value violates unique constraint" in str(ex)

    def test_insert_new_card_but_with_not_unique_email_should_raise_error(self):
        check = SubscriptionModel(
            card="A123", name="Some name", tar_type_id=1, email="A123@abv.bg"
        )
        db.session.add(check)
        db.session.commit()
        with pytest.raises(IntegrityError) as ex:
            check = SubscriptionModel(
                card="A123", name="Some name", tar_type_id=1, email="A123@abv.bg"
            )
            db.session.add(check)
            db.session.commit()
        assert "duplicate key value violates unique constraint" in str(ex)

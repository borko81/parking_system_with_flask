import datetime
import json

from flask_testing import TestCase

from config import create_app
from db import db
from models import ParkModel
from models.pay_type import PayType
from tests.base import generate_token
from tests.factories import AdminUserFactory
from tests.helpers_for_tests import GenerateTarifeData


class TestPaymentResource(TestCase):
    def create_app(self):
        return create_app("config.TestingConfig")

    def setUp(self):
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(self.app)
        db.create_all()
        self.user = AdminUserFactory()
        self.token = generate_token(self.user)
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "Application/json",
        }
        GenerateTarifeData.generate_all_needed_data()
        p = PayType(name="cash")
        db.session.add(p)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_pay_in_cash_when_all_is_ok_should_write_to_db(self):
        """
        Insertt new card, try to pay, should raise error, because card not leaving,
        after that change status to leave, try again to pay, return success. Try again
        to pay already payed card, should raise error.
        :return:
        """
        data = {"card": "A123"}
        self.path = "/parking"
        self.path_to_pay = "/parking/1/cash"
        response = self.client.post(
            headers=self.headers, path=self.path, data=json.dumps(data)
        )
        test_card_after_update = ParkModel.query.filter_by(id=1).first()
        test_card_after_update.income = (
            test_card_after_update.income - datetime.timedelta(hours=1)
        )

        # Test to pay card when card not leave yet from parking, should raise error
        response = self.client.post(headers=self.headers, path=self.path_to_pay)
        assert response.status_code == 400
        assert response.json["message"] == "This card not have bill yet"

        response = self.client.post(
            headers=self.headers, path=self.path, data=json.dumps(data)
        )
        test_card_after_update = ParkModel.query.filter_by(id=1).first()

        response = self.client.post(headers=self.headers, path=self.path_to_pay)
        assert response.status_code == 200
        assert (
            response.json == f"Success pay id: 1, sum: {test_card_after_update.price}."
        )

        # Test pay already pay card, should raise error
        response = self.client.post(headers=self.headers, path=self.path_to_pay)
        assert response.status_code == 400
        assert response.json["message"] == "This bill already is payed"

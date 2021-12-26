import json

from decouple import config
from flask_testing import TestCase

from config import create_app
from db import db
from models.pay_type import PayType
from tests.base import generate_token
from tests.factories import AdminUserFactory


class TestInsertNewPAymnetMethods(TestCase):
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

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_try_insert_new_payment_type(self):
        data = {"name": "Check"}
        path = "/pay_type"
        assert len(PayType.query.all()) == 0
        response = self.client.post(path, data=json.dumps(data), headers=self.headers)
        assert len(PayType.query.all()) == 1
        assert response.status_code, 201
        assert response.json == {"name": "Check", "id": 1}

        # Try to duplicate name
        response = self.client.post(path, data=json.dumps(data), headers=self.headers)
        assert response.status_code == 400
        assert len(PayType.query.all()) == 1

    def test_try_to_insert_new_paymnet_with_wrong_parameters(self):
        data = {"unused_name": "Check"}
        path = "/pay_type"
        assert len(PayType.query.all()) == 0
        response = self.client.post(path, data=json.dumps(data), headers=self.headers)
        assert response.status_code == 400
        assert response.json == {
            "message": "Invalid fields {'name': ['Missing data for required field.'], 'unused_name': ['Unknown field.']}"
        }

    def test_try_to_insert_new_paymnet_with_valid_param_but_wrong_length(self):
        length_name = config("PAY_TYPE_LENGTH")
        length_name_with_one = int(length_name) + 1
        data = {"name": f"{'c' * length_name_with_one}"}
        path = "/pay_type"
        assert len(PayType.query.all()) == 0
        response = self.client.post(path, data=json.dumps(data), headers=self.headers)
        assert response.status_code == 400
        assert (
            response.json["message"]
            == "Invalid fields {'name': ['Longer than maximum length %s.']}"
            % length_name
        )

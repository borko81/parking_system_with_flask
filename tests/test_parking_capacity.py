import json

from flask_testing import TestCase

from config import create_app
from db import db
from tests.base import generate_token
from tests.factories import AdminUserFactory


class TestCapacity(TestCase):
    def create_app(self):
        return create_app("config.TestingConfig")

    def setUp(self):
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(self.app)
        db.create_all()
        self.user = AdminUserFactory()
        self.token = generate_token(self.user)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_show_capacity(self):
        response = self.client.get("/parking_info")
        assert response.status_code == 400
        assert json.loads(response.data)["message"] == "Enter parking capacity"

    def test_insert_new_capacity_when_not_have_valid_token(self):
        response = self.client.post(
            "/parking/capacity", data=json.dumps({"capacity": 100})
        )
        assert response.status_code, 201
        assert json.loads(response.data)["message"] == "Invalid or missing token"

    def test_insert_new_capacity_when_have_valid_token_but_not_have_valid_data_raise_error(
        self,
    ):

        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.post(
            "/parking/capacity", data=json.dumps({"capacity": 100}), headers=headers
        )
        assert response.status_code, 201
        assert (
            json.loads(response.data)["message"]["capacity"] == "Capacity is required"
        )

    def test_insert_new_capacity_when_have_valid_token_and_have_valid_data(self):

        url_with_free_park_slot = "/parking_info"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "content-type": "application/json",
        }
        response = self.client.post(
            "/parking/capacity", data=json.dumps({"capacity": 100}), headers=headers
        )
        assert response.status_code, 201
        assert json.loads(response.data)["message"] == "Success insert parking capacity"

        # Continue test to show correct information to user, without weather,
        # this information has stopped by app configuration

        response = self.client.get(url_with_free_park_slot)
        assert response.status_code == 200
        assert response.json["Free Park Slot"] == 100

    def test_delete_capacity_when_have_already_row(self):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "content-type": "application/json",
        }
        self.test_insert_new_capacity_when_have_valid_token_and_have_valid_data()
        response = self.client.delete("/parking/capacity", headers=headers)
        assert response.status_code, 204

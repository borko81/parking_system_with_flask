import json

from flask_testing import TestCase

from config import create_app
from db import db
from models.users import UserModel
from tests.base import generate_token
from tests.factories import AdminUserFactory


class TestUserRegisterUrl(TestCase):
    def create_app(self):
        return create_app("config.TestingConfig")

    def setUp(self):
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(self.app)
        db.create_all()
        user = AdminUserFactory()
        self.token = generate_token(user)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

    def test_get_user_information_by_id_update_info_and_delete_user_all_happy_case(
        self,
    ):
        """
        Test get user information by id, next use put method to change some data, at the end delete user
        and check is everything is ok. All data is valid!!!!
        At the end try to delete user with invalid id, raise error
        """

        self.url = "/user/1"

        assert len(UserModel.query.all()) == 1

        new_user = UserModel(name="T T T", password="A123")
        db.session.add(new_user)
        db.session.commit()

        assert len(UserModel.query.all()) == 2
        resp = self.client.get(self.url, headers=self.headers)
        assert resp.status_code == 200
        assert resp.json["name"] == "T T T"

        resp_put = self.client.put(
            self.url,
            headers=self.headers,
            data=json.dumps({"name": "B B B", "password": "A123"}),
        )
        assert resp_put.status_code == 200
        assert resp_put.json["name"] == "B B B"
        assert resp_put.json["id"] == 1

        resp_delete = self.client.delete(self.url, headers=self.headers)
        assert resp_delete.status_code == 204
        assert len(UserModel.query.all()) == 1

        # Try to delete user with invalid id
        resp_error = self.client.delete(self.url, headers=self.headers)
        assert resp_error.status_code == 404
        assert resp_error.json["message"] == "Invalid id 1"

    def test_get_user_information_with_right_access(self):
        self.url = "/users"
        resp = self.client.get(self.url, headers=self.headers)
        assert resp.status_code == 200
        assert resp.json[0]["name"] == "Admin Admin Admin"
        assert resp.json[0]["type"] == "Admin"

    def tearDown(self):
        db.session.remove()
        db.drop_all()

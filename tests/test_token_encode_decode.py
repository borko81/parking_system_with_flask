import json

from flask_testing import TestCase

from config import create_app
from db import db
from managers.auth import AuthManager
from tests.base import generate_token
from tests.factories import AdminUserFactory


class TestTokenManager(TestCase):
    def create_app(self):
        return create_app("config.TestingConfig")

    def setUp(self):
        self.path_to_login = "/login"
        self.path_to_register = "/user/register"
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(self.app)
        db.create_all()
        self.user = AdminUserFactory()
        self.token = generate_token(self.user)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_correct_decode_token(self):
        self.data = {"name": "Boris Georgiev St", "password": "A123", "type": "staff"}
        new_user_response = self.client.post(
            self.path_to_register, headers=self.headers, data=json.dumps(self.data)
        )
        assert new_user_response.json == {
            "id": 1,
            "name": "Boris Georgiev St",
            "type": "staff",
        }

        login_response = self.client.post(
            self.path_to_login,
            headers={"Content-Type": "application/json"},
            data=json.dumps({"name": "Boris Georgiev St", "password": "A123"}),
        )
        token = login_response.json["token"]
        decode_token = AuthManager.decode_token(token)
        assert decode_token == (1, "Staff")

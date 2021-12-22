import json
from unittest.mock import patch

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

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    @patch("services.send_email_with_gmail.send_email_notification")
    def test_try_to_register_new_user_privileg_is_right_but_password_is_incorect(
        self, mock_email
    ):
        user = AdminUserFactory()
        self.token = generate_token(user)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }
        url = "/user/register"
        assert len(UserModel.query.all()) == 1
        data = {"name": "Boris1 G St", "password": "123"}
        resp = self.client.post(url, headers=self.headers, data=json.dumps(data))
        assert resp.status_code == 400
        assert len(UserModel.query.all()) == 1
        assert "Not valid password try again" in resp.json["message"]

    @patch("services.send_email_with_gmail.send_email_notification")
    def test_try_to_register_new_user_right_is_ok_but_username_not_valid(
        self, mock_email
    ):
        user = AdminUserFactory()
        self.token = generate_token(user)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }
        url = "/user/register"
        assert len(UserModel.query.all()) == 1
        data = {"name": "Boris", "password": "A123"}
        resp = self.client.post(url, headers=self.headers, data=json.dumps(data))
        assert resp.status_code == 400
        assert len(UserModel.query.all()) == 1
        assert "Username must have three name" in resp.json["message"]

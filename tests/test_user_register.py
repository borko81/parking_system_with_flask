import json
from unittest.mock import patch

from flask_testing import TestCase

from config import create_app
from db import db
from models.users import UserModel
from services.amazon_ses_services import SeSEmail
from tests.base import generate_token
from tests.factories import AdminUserFactory, StaffUserFactory


class TestUserRegisterUrl(TestCase):
    def create_app(self):
        return create_app("config.TestingConfig")

    def setUp(self):
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(self.app)
        db.create_all()

    @patch.object(SeSEmail, "send_email", return_value="None")
    def test_user_successfully_register_all_data_is_valid_add_user_in_db_also_try_to_login_with_new_user(
        self, mock_email
    ):
        """
        Test register user with valid privilegs, after that try to login this user
        check token is a part of response.
        """
        user = AdminUserFactory()
        self.token = generate_token(user)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }
        url = "/user/register"
        assert len(UserModel.query.all()) == 1
        data = {"name": "Boris G St", "password": "A123"}
        resp = self.client.post(url, headers=self.headers, data=json.dumps(data))
        assert resp.status_code == 201
        assert len(UserModel.query.all()) == 2
        resp_status = dict(resp.json)
        assert resp_status == {"type": "Staff", "id": 1, "name": "Boris G St"}
        check_user = UserModel.query.filter_by(id=1).first()
        assert "sha256" in check_user.password

        resp_for_login = self.client.post(
            "/login",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"name": "Boris G St", "password": "A123"}),
        )
        assert resp_for_login.status_code == 200
        assert "token" in resp_for_login.json

        resp_for_invalid_login = self.client.post(
            "/login",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"name": "Boris G St", "password": "A1243"}),
        )
        assert resp_for_invalid_login.status_code == 400
        assert "token" not in resp_for_invalid_login.json
        assert resp_for_invalid_login.json["message"] == "Invalid credential"

    @patch.object(SeSEmail, "send_email", return_value="None")
    def test_try_to_register_new_user_without_admin_privileg_should_raise_error(
        self, mock_email
    ):
        user = StaffUserFactory()
        self.token = generate_token(user)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }
        url = "/user/register"
        assert len(UserModel.query.all()) == 1
        data = {"name": "Boris G St", "password": "A123"}
        resp = self.client.post(url, headers=self.headers, data=json.dumps(data))
        assert resp.status_code == 403
        assert len(UserModel.query.all()) == 1
        assert (
            resp.json["message"] == "You do not have the rights to access this resource"
        )

    def tearDown(self):
        db.session.remove()
        db.drop_all()

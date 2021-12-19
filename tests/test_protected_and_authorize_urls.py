import json

from flask_testing import TestCase

from config import create_app
from db import db
from tests.base import generate_token
from tests.factories import StaffUserFactory


class TestNeededLoginUrl(TestCase):
    def create_app(self):
        return create_app("config.TestingConfig")

    def setUp(self):
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(self.app)
        db.create_all()
        user = StaffUserFactory()
        self.token = generate_token(user)
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_protected_url(self):
        resp = None
        for method, url in [
            ("GET", "/documents"),
            ("POST", "/documents"),
            ("POST", "/user/register"),
            ("GET", "/users"),
            ("DELETE", "/user/1"),
            ("GET", "user/1"),
            ("PATCH", "user/1"),
            ("PUT", "/tarif/price/3"),
            ("DELETE", "/tarif/price/6"),
            ("POST", "/tarif/price"),
            ("POST", "/tarif"),
            ("DELETE", "/pay_type/4"),
            ("POST", "/pay_type"),
            ("POST", "/parking/capacity"),
            ("PUT", "/parking/capacity"),
            ("DELETE", "/parking/capacity"),
            ("GET", "/subscription"),
            ("GET", "/subscription/231"),
            ("DELETE", "/subscription/211"),
            ("POST", "/subscription"),
            ("PUT", "/subscription/21"),
            ("GET", "/parking"),
            ("GET", "/parking/detail/86"),
            ("DELETE", "/parking/detail/84"),
            ("PUT", "/parking/detail/86"),
            ("POST", "/parking"),
            ("POST", "/parking/78/wise"),
            ("POST", "/parking/88/cash"),
            ("GET", "/transactions"),
            ("GET", "/transaction?id=3"),
            ("GET", "/transaction?trans_id=50320289"),
            ("POST", "/otc"),
            ("GET", "/otc/5"),
            ("GET", "/documents"),
            ("POST", "/documents"),
        ]:
            if method == "GET":
                resp = self.client.get(url)
            elif method == "POST":
                resp = self.client.post(url, data=json.dumps({}))
            elif method == "PUT":
                resp = self.client.put(url, data=json.dumps({}))
            elif method == "PATCH":
                resp = self.client.patch(url, data=json.dumps({}))
            elif method == "DELETE":
                resp = self.client.delete(url)
            self.assert401(resp)

    def test_admin_protected_urls(self):
        resp = None
        for method, url in [
            ("GET", "/documents"),
            ("POST", "/documents"),
            ("PUT", "/parking/detail/86"),
            ("POST", "/parking/capacity"),
            ("PUT", "/parking/capacity"),
            ("DELETE", "/parking/capacity"),
            ("DELETE", "/pay_type/4"),
            ("POST", "/pay_type"),
            ("POST", "/tarif/price"),
            ("POST", "/tarif"),
            ("GET", "/transactions"),
            ("GET", "/transaction?id=3"),
        ]:

            if method == "POST":
                resp = self.client.post(url, data=json.dumps({}), headers=self.headers)
            if method == "PUT":
                resp = self.client.put(url, data=json.dumps({}), headers=self.headers)
            elif method == "DELETE":
                resp = self.client.delete(url, headers=self.headers)
            elif method == "GET":
                resp = self.client.get(url, headers=self.headers)
            self.assert403(resp)

import json

from flask_testing import TestCase

from config import create_app
from db import db
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

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_try_insert_new_payment_method(self):
        pass
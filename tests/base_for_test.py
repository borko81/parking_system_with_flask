from flask_testing import TestCase

from config import create_app
from db import db
from tests.base import generate_token
from tests.factories import AdminUserFactory, StaffUserFactory


class BaseForTests(TestCase):
    def create_app(self):
        return create_app("config.TestingConfig")

    def setUp(self):
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(self.app)
        db.create_all()
        self.user_admin = AdminUserFactory()
        self.token_admin = generate_token(self.user_admin)
        self.user_staff = StaffUserFactory()
        self.token_staff = generate_token(self.user_staff)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

import json
from unittest.mock import patch

from flask_testing import TestCase

from config import create_app
from constants import photo_url, photo_ext
from db import db
from models.subscription import SubscriptionModel
from models.tarif_type import TariffTypeModel
from services.cloudinary_upload import Cloudinary
from tests.base import generate_token
from tests.factories import StaffUserFactory, SubscribeFactory


class TestSubscribe(TestCase):
    def create_app(self):
        return create_app("config.TestingConfig")

    def setUp(self):
        self.path_to_subscribe = "/subscription"
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(self.app)
        db.create_all()
        self.user = StaffUserFactory()
        self.token = generate_token(self.user)
        self.type = TariffTypeModel(name="common")
        db.session.add(self.type)
        db.session.commit()
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "Application/json",
        }

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_insert_new_subscribe_all_data_is_valid_get_only_needed_field_write_to_db(
        self,
    ):
        data_for_common = {"card": "C123", "tar_type_id": 1, "email": "c123@abv.bg"}
        response = self.client.post(
            self.path_to_subscribe,
            headers=self.headers,
            data=json.dumps(data_for_common),
        )
        assert response.status_code == 201
        assert len(SubscriptionModel.query.all()) == 1

        # Test get return subscribers with get method
        response = self.client.get(self.path_to_subscribe, headers=self.headers)
        assert response.status_code == 200
        expected_data = dict(json.loads(response.data)[0])

        # Remove dates from response
        expected_data.pop("active_date_from")
        expected_data.pop("active_date_to")

        assert expected_data == {
            "card": "C123",
            "email": "c123@abv.bg",
            "id": 1,
            "name": "",
            "photo_ext": None,
            "photo_url": None,
            "tar_type_id": 1,
        }

    @patch.object(Cloudinary, "upload_picture_to_cloudinary", return_value="None")
    def test_insert_new_subscribe_all_data_is_valid_get_all_field_write_to_db(
        self, mock_cloudinary
    ):

        data_for_common = {
            "card": "C123",
            "tar_type_id": 1,
            "email": "c123@abv.bg",
            "name": "Test Car",
            "active_date_to": "2022-01-22",
            "photo_url": photo_url,
            "photo_ext": photo_ext,
        }

        response = self.client.post(
            self.path_to_subscribe,
            headers=self.headers,
            data=json.dumps(data_for_common),
        )
        assert response.status_code == 201
        assert response.json["message"] == {
            "message": "Successfully added card with id 1"
        }

        test_subsc = SubscriptionModel.query.filter_by(id=1).first()
        assert test_subsc.card == "C123"

        # Test insert again but not unique card, should raise error
        data_for_common = {
            "card": "C123",
            "tar_type_id": 1,
            "email": "c123@abv.bg",
            "name": "Test Car",
            "active_date_to": "2022-01-22",
            "photo_url": photo_url,
            "photo_ext": photo_ext,
        }
        response = self.client.post(
            self.path_to_subscribe,
            headers=self.headers,
            data=json.dumps(data_for_common),
        )
        assert response.status_code == 400
        assert response.json["message"] == "Card already exists"

        # Test insert again but not unique email, should raise error
        data_for_common = {
            "card": "C1234",
            "tar_type_id": 1,
            "email": "c123@abv.bg",
            "name": "Test Car",
            "active_date_to": "2022-01-22",
            "photo_url": photo_url,
            "photo_ext": photo_ext,
        }
        response = self.client.post(
            self.path_to_subscribe,
            headers=self.headers,
            data=json.dumps(data_for_common),
        )
        assert response.status_code == 400
        assert response.json["message"] == "Email is used with another card"

    @patch.object(Cloudinary, "upload_picture_to_cloudinary", return_value="None")
    def test_insert_new_subscribe_with_invalid_data(self, mock_cloudinary):
        data_for_common = {
            "card": "C123",
        }
        response = self.client.post(
            self.path_to_subscribe,
            headers=self.headers,
            data=json.dumps(data_for_common),
        )
        assert response.status_code == 400
        assert len(SubscriptionModel.query.all()) == 0
        assert response.json == {
            "message": "Invalid fields {'tar_type_id': ['Missing data for required field.']}"
        }

        data_for_common = {
            "tar_type_id": 1,
        }
        response = self.client.post(
            self.path_to_subscribe,
            headers=self.headers,
            data=json.dumps(data_for_common),
        )
        assert response.status_code == 400
        assert len(SubscriptionModel.query.all()) == 0
        assert response.json == {
            "message": "Invalid fields {'card': ['Missing data for required field.']}"
        }

    def test_return_details_also_test_delete_method(self):
        subscribe = SubscribeFactory()
        response = self.client.get(self.path_to_subscribe + "/1", headers=self.headers)
        assert response.status_code == 200

        # Test get invalid id raise error 404
        response = self.client.get(self.path_to_subscribe + "/2", headers=self.headers)
        assert response.status_code == 404
        assert response.json["message"] == "Invalid id 2"

        assert len(SubscriptionModel.query.all()) == 1

        # Test to delete invalid data
        response = self.client.delete(
            self.path_to_subscribe + "/2", headers=self.headers
        )
        assert response.status_code == 404

        # Test to delete subscriber with valid id
        response = self.client.delete(
            self.path_to_subscribe + "/1", headers=self.headers
        )
        assert response.status_code == 204
        assert len(SubscriptionModel.query.all()) == 0

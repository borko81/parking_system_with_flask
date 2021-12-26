import json

from flask_testing import TestCase

from config import create_app
from db import db
from models import TariffTypeModel
from tests.base import generate_token
from tests.factories import AdminUserFactory


class TestTarife(TestCase):
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
        self.path = "/tarif"
        self.path_for_insert_price_for_hour = "/tarif/price"
        self.path_to_get_all_price = "/tarif/price"
        self.path_to_get_all_price_for_type = "/tarif/type/vip"
        self.path_to_get_all_price_for_invalid_type = "/tarif/type/invalid"

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_new_tarife_name_is_correct_and_insert_into_database_also_test_insert_price(
        self,
    ):
        """
        Insert new tarife name with name in Enum, check is new name correct insert to DB
        after that test to create new price, frist is with good data, next try to insert
        price with unknown tarif_id, should raise 404, next test schema validator for new price create
        Finally return price for name that already in base, should return result, when name not in DB, should
        raise error 404.
        """
        data_for_common = {"name": "common"}
        data_for_vip = {"name": "vip"}
        data_with_price = {"tarif_id": 2, "price": 1, "stay": "00:01"}
        assert len(TariffTypeModel.query.all()) == 0
        response = self.client.post(
            self.path, headers=self.headers, data=json.dumps(data_for_common)
        )
        assert response.status_code == 201
        assert len(TariffTypeModel.query.all()) == 1
        assert response.json == {"name": "common", "id": 1}
        response = self.client.post(
            self.path, headers=self.headers, data=json.dumps(data_for_vip)
        )
        assert response.status_code == 201
        assert response.json == {"name": "vip", "id": 2}

        # Return information for newly created self, return this information
        response = self.client.get(self.path)
        assert response.status_code == 200
        assert response.json == {
            "all_tarife": [{"name": "Common", "id": 1}, {"name": "Vip", "id": 2}]
        }

        # Test to insert new price
        response = self.client.post(
            self.path_for_insert_price_for_hour,
            headers=self.headers,
            data=json.dumps(data_with_price),
        )
        assert response.status_code == 201
        assert response.json == {"stay": "00:01", "price": 1, "tarif_id": 2}

        # Test to insert new price with unknown name should raise Error 400
        response = self.client.post(
            self.path_for_insert_price_for_hour,
            headers=self.headers,
            data=json.dumps({"tarif_id": 21, "price": 1, "stay": "00:01"}),
        )
        assert response.status_code == 400
        assert response.json["message"] == "This type is not valid"

        # Test schema raise error when try to insert new price tarif_id is missing
        response = self.client.post(
            self.path_for_insert_price_for_hour,
            headers=self.headers,
            data=json.dumps({"Error": 2, "price": 1, "stay": "00:01"}),
        )
        assert response.status_code == 400
        assert (
            response.json["message"]
            == "Invalid fields {'tarif_id': ['Missing data for required field.'], 'Error': ['Unknown field.']}"
        )

        # Test schema raise error when try to insert new price name is missing
        response = self.client.post(
            self.path_for_insert_price_for_hour,
            headers=self.headers,
            data=json.dumps({"tarif_id": 2, "Error": 1, "stay": "00:01"}),
        )
        assert response.status_code == 400
        assert (
            response.json["message"]
            == "Invalid fields {'price': ['Missing data for required field.'], 'Error': ['Unknown field.']}"
        )

        # Test schema raise error when try to insert new price price is missing
        response = self.client.post(
            self.path_for_insert_price_for_hour,
            headers=self.headers,
            data=json.dumps({"tarif_id": 2, "price": 1, "Error": "00:01"}),
        )
        assert response.status_code == 400
        assert (
            response.json["message"]
            == "Invalid fields {'stay': ['Missing data for required field.'], 'Error': ['Unknown field.']}"
        )

        # Test to return price info
        response = self.client.get(
            self.path_to_get_all_price, headers={"Content-Type": "Application/json"}
        )
        assert response.status_code == 200
        assert response.json == [{"stay": "00:01", "price": 1, "tarif_id": 2}]

        # Test to return all price for concrete name type
        response = self.client.get(
            self.path_to_get_all_price_for_type,
            headers={"Content-Type": "Application/json"},
        )
        assert response.status_code == 200
        assert response.json == [{"stay": "00:01", "price": 1, "tarif_id": 2}]

        # Test raise BadRequest when try to return unknown name of type
        response = self.client.get(
            self.path_to_get_all_price_for_invalid_type,
            headers={"Content-Type": "Application/json"},
        )
        assert response.status_code == 404


    def test_create_new_tarife_with_name_not_recognize_in_enum_should_raise_BadRequest(
        self,
    ):
        data_for_common = {"name": "Test"}
        response = self.client.post(
            self.path, headers=self.headers, data=json.dumps(data_for_common)
        )
        assert response.status_code == 400
        assert response.json["message"] == "That name not valid"
        assert len(TariffTypeModel.query.all()) == 0

    def test_create_new_tarife_with_not_corect_data_should_raise_BadRequest(self):
        data_for_common = {"price": "Test"}
        response = self.client.post(
            self.path, headers=self.headers, data=json.dumps(data_for_common)
        )
        assert response.status_code == 400
        assert (
            response.json["message"]
            == "Invalid fields {'name': ['Missing data for required field.'], 'price': ['Unknown field.']}"
        )
        assert len(TariffTypeModel.query.all()) == 0

import datetime
import json

from flask_testing import TestCase

from config import create_app
from db import db
from managers.park_capacity_manager import ParkCapacityManager
from managers.park_manager import ParkingManager
from models import (
    SubscriptionModel,
    ParkModel,
)
from tests.base import generate_token
from tests.factories import AdminUserFactory
from tests.helpers_for_tests import GenerateTarifeData

income = datetime.datetime.now()


# @freeze_time("2012-12-28 15:19:00.00")
class TestParkingSystem(TestCase):
    def create_app(self):
        return create_app("config.TestingConfig")

    def setUp(self):
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.init_app(self.app)
        db.create_all()
        self.user = AdminUserFactory()
        self.token = generate_token(self.user)

        self.headers = {
            "Content-Type": "Application/json",
            "Authorization": f"Bearer {self.token}",
        }

        self.path = "/parking"
        self.path_to_change = "/parking/detail/1"

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_insert_new_card_after_that_insert_same_card_again_must_be_updated_free_slot_must_be_decrese_and_increase(
        self,
    ):
        """
        Insert new card, card is checking in subscriber or not, after that, insert same card number
        data must be change, price is update and leave time too.
        """
        GenerateTarifeData.generate_all_needed_data()
        data = {"card": "A123"}
        response = self.client.post(
            headers=self.headers, path=self.path, data=json.dumps(data)
        )
        assert response.status_code == 201

        # Test free capacity is reduced after insert new card
        assert (
            ParkCapacityManager.get_capacity().capacity
            - len(ParkingManager.show_car_in_park())
            == 1
        )

        # TODO not understand how to use freezgun with func.now()
        # assert response.json == {"card": "A123", "id": 1, "income": str(datetime.datetime.now())}
        response = self.client.get(headers=self.headers, path=self.path)
        assert response.status_code == 200
        assert len(ParkModel.query.all()) == 1
        check = ParkModel.query.filter_by(id=1).first()
        assert check.outcome == None
        assert check.price == None
        assert check.card == "A123"

        # Make new response, with same card, but stay is less the 1 minute
        response = self.client.post(
            headers=self.headers, path=self.path, data=json.dumps(data)
        )
        assert response.status_code == 400
        assert (
            response.json["message"]
            == "This card stay less then 1 minute, you may want to delete record with id 1"
        )

        # Change time of entered card, next is another try to leave the card, time has changes with 1 hour
        updated_data_data = {
            "pay": False,
            "tarif_id": 1,
            "price": None,
            "outcome": None,
            "otc_id": None,
            "income": datetime.datetime.now() - datetime.timedelta(hours=1),
            "card": "A123",
            "id": 1,
        }

        # Another try to leave the card from park
        test_card_after_update = ParkModel.query.filter_by(id=1).first()
        test_card_after_update.income = (
            test_card_after_update.income - datetime.timedelta(hours=1)
        )
        response = self.client.post(
            headers=self.headers, path=self.path, data=json.dumps(data)
        )
        assert response.status_code == 200
        test_card_after_update = ParkModel.query.filter_by(id=1).first()
        assert test_card_after_update.price == 1

        # Test capacity is increase after successfully leave the card
        # Test free capacity is reduced after insert new card
        assert (
            ParkCapacityManager.get_capacity().capacity
            - len(ParkingManager.show_car_in_park())
            == 2
        )

    def test_insert_invalid_card_number_should_raise_error(self):
        GenerateTarifeData.generate_all_needed_data()
        data = {"card": "A1234"}
        response = self.client.post(
            headers=self.headers, path=self.path, data=json.dumps(data)
        )
        assert response.status_code == 404
        assert (
            response.json["message"]
            == "This card not found on server, try with another"
        )

    def test_insert_valid_card_number_but_with_not_valid_time_should_raise_error(self):
        GenerateTarifeData.generate_all_needed_data()
        s = SubscriptionModel(
            card="A1234",
            email="1234@abv.bg",
            tar_type_id=1,
            active_date_to="2021-12-20",
        )
        db.session.add(s)
        db.session.commit()
        data = {"card": "A1234"}
        response = self.client.post(
            headers=self.headers, path=self.path, data=json.dumps(data)
        )
        assert response.status_code == 400
        assert response.json["message"] == "This card is nо longer valid"

    def test_try_to_insert_more_than_parking_capacity_card_should_raise_error(self):
        GenerateTarifeData.generate_all_needed_data()
        s = SubscriptionModel(card="A1234", email="1234@abv.bg", tar_type_id=1)
        db.session.add(s)
        db.session.commit()
        s = SubscriptionModel(card="A12345", email="12345@abv.bg", tar_type_id=1)
        db.session.add(s)
        db.session.commit()
        data_one = {"card": "A123"}
        data_two = {"card": "A1234"}
        data_three = {"card": "A12345"}
        response = self.client.post(
            headers=self.headers, path=self.path, data=json.dumps(data_one)
        )
        assert response.status_code == 201
        response = self.client.post(
            headers=self.headers, path=self.path, data=json.dumps(data_two)
        )
        assert response.status_code == 201
        response = self.client.post(
            headers=self.headers, path=self.path, data=json.dumps(data_three)
        )
        assert response.status_code == 400
        assert response.json["message"] == "Not Enough space in park"

    def test_delete_card_from_parking_when_this_card_not_payed_yet_should_remove(self):
        GenerateTarifeData.generate_all_needed_data()
        data = {"card": "A123"}
        path_to_test_delete = "/parking/detail/1"
        response = self.client.post(
            headers=self.headers, path=self.path, data=json.dumps(data)
        )
        assert len(ParkModel.query.all()) == 1
        response = self.client.delete(headers=self.headers, path=path_to_test_delete)
        assert len(ParkModel.query.all()) == 0
        assert response.json == 204

    def test_delete_card_from_parking_when_card_already_been_payed_should_raise_error(
        self,
    ):
        GenerateTarifeData.generate_all_needed_data()
        data = {"card": "A123"}
        path_to_test_delete = "/parking/detail/1"
        response = self.client.post(
            headers=self.headers, path=self.path, data=json.dumps(data)
        )
        card_update = ParkModel.query.filter_by(id=1).first()
        card_update.pay = True
        assert len(ParkModel.query.all()) == 1
        response = self.client.delete(headers=self.headers, path=path_to_test_delete)
        assert len(ParkModel.query.all()) == 1
        assert response.json["message"] == "Card is already payed, not allow editing!"

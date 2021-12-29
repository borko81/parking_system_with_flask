from flask import request
from flask_restful import Resource

from helpers.decorator import validate_schema, permission_required
from managers.auth import auth
from managers.park_manager import ParkingManager
from managers.parking_detail_id_manager import ParkingDetailFromIdManager
from models import UserType
from schemas.parking_schemas import ParkEnterSchema
from schemas.request.park_request_schema import ParkRequestSchemaForEdit
from schemas.response.park_response_schema import ParkResponseSchema as park_res_schema


class ParkingRes(Resource):
    @auth.login_required
    def get(self):
        """
        Returns all cards that are still in the parking lot and have not paid
        ---
        tags:
        - Park
        parameters:
        - name: Authorization
          in: header
        responses:
          200:
            description: Ok
          401:
            description: Unauthorized
        """
        return ParkingManager.show_car_in_park()

    @auth.login_required
    @validate_schema(ParkEnterSchema)
    def post(self):
        """
        Adds a new card in the parking lot, if the card is already there
        and has not been paid yet, the information with the financial part is updated
        ---
        tags:
        - Park
        parameters:
        - name: Authorization
          in: header
        - name: data
          in: body
        responses:
          201:
            description: success
          200:
            description: ok
          401:
            description: Unauthorized
          400:
            description: This card stay less then 1 minute
        """
        data = request.get_json()
        return ParkingManager.input_new_car_in_park(data)


class ParkingDetailInfoRes(Resource):
    @staticmethod
    def return_result_in_json_use_schema(result):
        """Validate result to json (helper module)"""
        schema = park_res_schema()
        return schema.dump(result.first())

    @auth.login_required
    def get(self, _id):
        """
        Return information for card by parking id
        ---
        tags:
        - Park
        parameters:
        - name: Authorization
          in: header
        - name: _id
          in: path
        responses:
          200:
            description: ok
          401:
            description: Unauthorized
          404:
            description: Not Found
        """
        result = ParkingDetailFromIdManager.get_from_id(_id)
        return ParkingDetailInfoRes.return_result_in_json_use_schema(result)

    @auth.login_required
    @permission_required(UserType.admin)
    @validate_schema(ParkRequestSchemaForEdit)
    def put(self, _id):
        """
        If card found in park and card not already is payed, may edit some information.
        Edint allowed only with admin rights.
        ---
        tags:
        - Park
        parameters:
        - name: Authorization
          in: header
        - name: _id
          in: path
        - name: data
          in: body
        responses:
          200:
            description: ok
          401:
            description: Unauthorized
        """
        data = request.get_json()
        result = ParkingDetailFromIdManager.edit_car_in_park(_id, data)
        return self.return_result_in_json_use_schema(result), 200

    @auth.login_required
    def delete(self, _id):
        """
        if found in park card with this id, may delete only from admin user
        and only if card not already is payed
        ---
        tags:
        - Park
        parameters:
        - name: Authorization
          in: header
        - name: _id
          in: path
        responses:
          204:
            description: ok
          401:
            description: Unauthorized
          404:
            description: Not Found
        """
        return ParkingDetailFromIdManager.delete_car_in_park(_id)


class ParkingPayRes(Resource):
    def post(self):
        pass


class ParkingAlreadyPay(Resource):
    def get(self):
        pass

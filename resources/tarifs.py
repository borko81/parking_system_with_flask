from flask import request
from flask_restful import Resource

from helpers.decorator import validate_schema, permission_required
from managers.auth import auth
from managers.tarif import TarifAllManager
from managers.tarif_price_manager import (
    TarifPricesManager,
    TarifPriceFromConcretTypeManager,
    PriceForConcretTypeManager,
)
from models import UserType
from schemas.request.tarif_price import TarifPriceRequestSchema
from schemas.request.tarifl import TartifRequestSchema


class TarifAllRes(Resource):
    def get(self):
        """
        Return all tarif plan
        ---
        tags:
        - Tarife plan
        responses:
          200:
            description: Return users info
            examples:
              url: /user/10
        """
        data = TarifAllManager.get_all_tarif()
        return {"all_tarife": data}, 200

    @auth.login_required
    @permission_required(UserType.admin)
    @validate_schema(TartifRequestSchema)
    def post(self):
        """
        Post new tarife
        ---
        tags:
        - Tarife plan
        parameters:
        - name: Authorization
          in: header
        - name: name
          in: body
        responses:
          201:
                description: Success
          401:
                description: Unauthorized
          400:
            description: That name not valid
        """
        data = request.get_json()
        return TarifAllManager.input_new_tarif(data)


class TarifPricesRes(Resource):
    def get(self):
        """
        Return all tarif price
        ---
        tags:
        - Tarife plan
        responses:
          200:
            description: OK
        """
        return TarifPricesManager.get_all_tarife_prices()

    @auth.login_required
    @permission_required(UserType.admin)
    @validate_schema(TarifPriceRequestSchema)
    def post(self):
        """
        Post new price
        ---
        tags:
        - Tarife plan
        parameters:
        - name: Authorization
          in: header
        - name: tarif_id
          in: body
        - name: price
          in: body
        - name: stay
          in: body
        responses:
          201:
                description: Success
          401:
                description: Unauthorized
        """
        data = request.get_json()
        return TarifPricesManager.input_new_price(data)


class TarifConcretRes(Resource):
    def get(self, _id: int):
        """
        From given id return price info with this id, when id not valid return NotFound
        ---
        tags:
        - Tarife plan
        parameters:
        - name: _id
          in: path
        responses:
          200:
                description: OK
          404:
                description: Not found that id
        """
        schema = TarifPriceRequestSchema()
        return (
            schema.dump(TarifPriceFromConcretTypeManager.get_result(_id).first()),
            200,
        )

    @auth.login_required
    @permission_required(UserType.admin)
    def put(self, _id: int):
        """
        usage:  curl 127.0.0.1:5000/tarif/price/2 -X PUT -H "Content-Type:application/json" -d '{"price": 20}'
        :param _id: int
        :return: update data
        """
        data = request.get_json()
        schema = TarifPriceRequestSchema()
        return (
            schema.dump(
                TarifPriceFromConcretTypeManager.edit_result(_id, data).first()
            ),
            200,
        )

    @auth.login_required
    @permission_required(UserType.admin)
    def delete(self, _id: int):
        """
        From given id return price who may deleted
        ---
        tags:
        - Tarife plan
        parameters:
        - name: Authorization
          in: header
        - name: _id
          in: path
        responses:
          200:
                description: OK
          404:
                description: Not found that id
        """
        return TarifPriceFromConcretTypeManager.delete_result(_id)


class ReturnPricesFromConcretTypeRes(Resource):
    def get(self, type: str):
        """
        From given type return prices
        ---
        tags:
        - Tarife plan
        parameters:
        - name: Authorization
          in: header
        - name: type
          in: path
        responses:
          200:
                description: OK
          404:
                description: Not found that type
        """
        return PriceForConcretTypeManager.get_price_from_type(type)

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
        :usage: curl 127.0.0.1:5000/tarif
        :return: List with all tarif
        """
        data = TarifAllManager.get_all_tarif()
        return {"all_tarife": data}, 200

    @validate_schema(TartifRequestSchema)
    @auth.login_required
    @permission_required(UserType.admin)
    def post(self):
        data = request.get_json()
        return TarifAllManager.input_new_tarif(data)


class TarifPricesRes(Resource):
    def get(self):
        """
        usage: curl 127.0.0.1:5000/tarif/price
        :return: json data with all prices for stay
        """
        return TarifPricesManager.get_all_tarife_prices()

    @validate_schema(TarifPriceRequestSchema)
    @auth.login_required
    @permission_required(UserType.admin)
    def post(self):
        """
        usage:  curl 127.0.0.1:5000/tarif/price -X POST -H "Content-Type:application/json" -d '{"tarif_id": 2, "stay":"00:01", "price":1}'
        :return: json with new data
        """
        data = request.get_json()
        return TarifPricesManager.input_new_price(data)


class TarifConcretRes(Resource):
    def get(self, _id: int):
        """
        usage: curl 127.0.0.1:5000/tarif/price/2
        :param _id: int
        :return: json data with result
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
        return TarifPriceFromConcretTypeManager.delete_result(_id)


class ReturnPricesFromConcretTypeRes(Resource):
    def get(self, type: str):
        return PriceForConcretTypeManager.get_price_from_type(type)

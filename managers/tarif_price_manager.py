from werkzeug.exceptions import BadRequest

from db import db
from models.tarif_el import TarifPiceModel
from models.tarif_type import TariffTypeModel
from schemas.request.tarif_price import TarifPriceRequestSchema, PriceForConcretTarType


class TarifPricesManager:
    @staticmethod
    def input_new_price(data):
        schema = TarifPriceRequestSchema()
        result = TarifPiceModel(**data)
        db.session.add(result)
        db.session.flush()
        return schema.dump(result)

    @staticmethod
    def get_all_tarife_prices():
        schema = TarifPriceRequestSchema()
        result = TarifPiceModel.query.all()
        return schema.dump(result, many=True)


class TarifPriceFromConcretTypeManager:
    @staticmethod
    def get_result(_id):
        result = TarifPiceModel.query.filter_by(id=_id)
        if result.first():
            return result
        raise BadRequest("Invalid id")

    @staticmethod
    def edit_result(_id, data):
        price = TarifPriceFromConcretTypeManager.get_result(_id)
        price.update(data)
        return price

    @staticmethod
    def delete_result(_id):
        price = TarifPriceFromConcretTypeManager.get_result(_id)
        db.session.delete(price.first())
        return 204


class PriceForConcretTypeManager:
    @staticmethod
    def get_price_from_type(type):
        schema = PriceForConcretTarType()
        try:
            search_type = TariffTypeModel.query.filter_by(name=type).first()
            result = TarifPiceModel.query.filter_by(tarif_id=search_type.id)
            return schema.dump(result, many=True)
        except Exception:
            raise BadRequest("Invalid type")

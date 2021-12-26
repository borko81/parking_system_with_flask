from werkzeug.exceptions import NotFound, BadRequest

from db import db
from helpers.data_preparation import data_preparate_for_commit
from helpers.loger_config import custom_logger
from models import TariffTypeModel
from models.tarif_el import TarifPiceModel
from schemas.request.tarif_price import TarifPriceRequestSchema, PriceForConcretTarType


class TarifPricesManager:
    @staticmethod
    def input_new_price(data):
        if not TariffTypeModel.query.filter_by(id=data["tarif_id"]).first():
            custom_logger(
                "error",
                f"Function input_new_price: try to insert data with invalid type_id: {data['tarif_id']}",
            )
            raise BadRequest("This type is not valid")
        schema = TarifPriceRequestSchema()
        result = TarifPiceModel(**data)
        data_preparate_for_commit(result)
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
        raise NotFound("Invalid id")

    @staticmethod
    def edit_result(_id, data):
        price = TarifPriceFromConcretTypeManager.get_result(_id)
        price.update(data)
        return price

    @staticmethod
    def delete_result(_id):
        price = TarifPriceFromConcretTypeManager.get_result(_id)
        db.session.delete(price.first())
        custom_logger(
            "error",
            f"Function delete_result: delete price with id {_id}",
        )
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
            raise NotFound("Invalid type")

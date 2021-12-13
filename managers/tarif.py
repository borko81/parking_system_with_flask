from werkzeug.exceptions import BadRequest

from db import db
from models.tarif_type import TariffTypeModel
from models.enum import TarifTypeEnum
from schemas.response.tarif import TartifResponseSchema
from helpers.data_preparation import data_preparate_for_commit


class TarifAllManager:
    @staticmethod
    def get_all_tarif():
        data = TariffTypeModel.query.all()
        schema = TartifResponseSchema()
        return schema.dump(data, many=True)

    @staticmethod
    def input_new_tarif(data):
        if data["name"] not in [(i.value).lower() for i in TarifTypeEnum]:
            raise BadRequest("That name not valid")
        if TariffTypeModel.find_by_name(data["name"]).first() is None:
            new_tarife = TariffTypeModel(**data)
            data_preparate_for_commit(new_tarife)
            schema = TartifResponseSchema()
            return schema.dump(new_tarife), 201
        raise BadRequest("Error with unique variable")

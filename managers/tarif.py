from werkzeug.exceptions import BadRequest

from helpers.data_preparation import data_preparate_for_commit
from helpers.loger_config import custom_logger
from models.enum import TarifTypeEnum
from models.tarif_type import TariffTypeModel
from schemas.response.tarif import TartifResponseSchema


class TarifAllManager:
    @staticmethod
    def get_all_tarif():
        data = TariffTypeModel.query.all()
        schema = TartifResponseSchema()
        return schema.dump(data, many=True)

    @staticmethod
    def input_new_tarif(data):
        if data["name"] not in [(i.value).lower() for i in TarifTypeEnum]:
            custom_logger(
                "error",
                f"Function input_new_tarif: try to insert {data['name']} that name not in enumerator",
            )
            raise BadRequest("That name not valid")
        if TariffTypeModel.find_by_name(data["name"]).first() is None:
            new_tarife = TariffTypeModel(**data)
            data_preparate_for_commit(new_tarife)
            schema = TartifResponseSchema()
            return schema.dump(new_tarife), 201
        custom_logger(
            "error",
            f"Function input_new_tarif: try to insert duplicate name {data['name']}",
        )
        raise BadRequest("Error with unique variable")

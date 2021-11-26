from werkzeug.exceptions import BadRequest

from db import db
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
        if TariffTypeModel.find_by_name(data["name"]).first() is None:
            new_tarife = TariffTypeModel(**data)
            db.session.add(new_tarife)
            db.session.flush()
            schema = TartifResponseSchema()
            return schema.dump(new_tarife), 201
        raise BadRequest("Error with unique variable")

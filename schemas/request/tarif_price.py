from marshmallow import Schema, fields

from helpers.decorator import validate_stay
from schemas.response.tarif import TartifResponseSchema


class TarifPriceRequestSchema(Schema):
    tarif_id = fields.Integer(required=True)
    stay = fields.String(required=True, validate=validate_stay)
    price = fields.Integer(required=True)


class PriceForConcretTarType(TarifPriceRequestSchema):
    plan = fields.Nested(TartifResponseSchema(only=("name",)))

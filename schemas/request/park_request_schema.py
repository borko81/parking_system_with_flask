from decouple import config
from marshmallow import Schema, fields, validate


class ParkRequestSchema(Schema):
    card = fields.String(
        required=True,
        validate=validate.Length(max=config("PARK_CARD_FIELDS_LENGTH", cast=int)),
    )
    tarif_id = fields.Integer(required=True)


class ParkRequestSchemaForEdit(ParkRequestSchema):
    pay = fields.Boolean()
    id = fields.Integer()
    income = fields.DateTime(allow_none=True)
    outcome = fields.DateTime(allow_none=True)
    price = fields.Number(allow_none=True)
    otc_id = fields.Number(allow_none=True)

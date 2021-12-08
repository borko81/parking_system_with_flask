from decouple import config
from marshmallow import Schema, fields, validate


class PayTypeBaseSchema(Schema):
    name = fields.String(
        required=True, validate=validate.Length(max=config("PAY_TYPE_LENGTH", cast=int))
    )

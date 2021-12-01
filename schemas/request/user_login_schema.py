from decouple import config
from marshmallow import Schema, fields, validate


class UserLoginSchema(Schema):
    name = fields.String(
        required=True,
        validate=validate.Length(max=config("USER_NAME_FIELD_LENGTH", cast=int)),
    )
    password = fields.String(required=True)

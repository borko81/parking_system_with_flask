from marshmallow import Schema, fields


class UserLoginSchema(Schema):
    name = fields.String(required=True)
    password = fields.String(required=True)

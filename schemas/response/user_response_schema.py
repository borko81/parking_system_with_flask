from marshmallow import fields, Schema


class UserResponceSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    type = fields.String()

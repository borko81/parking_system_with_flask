from marshmallow import Schema, fields


class TartifResponseSchema(Schema):
    id = fields.Integer()
    name = fields.String()

from marshmallow import Schema, fields


class TartifRequestSchema(Schema):
    name = fields.String(required=True)

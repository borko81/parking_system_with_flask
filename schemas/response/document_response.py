from marshmallow import Schema, fields


class DocResponse(Schema):
    id = fields.Integer()
    name = fields.String(required=True)
    url = fields.String(required=True)
    create_on = fields.DateTime()
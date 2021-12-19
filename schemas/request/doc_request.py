from marshmallow import Schema, fields


class DocRequest(Schema):
    name = fields.String(required=True)
    ecoded_string = fields.String(required=True)
    ext = fields.String(required=True)
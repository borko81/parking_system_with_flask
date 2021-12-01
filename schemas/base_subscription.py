from marshmallow import Schema, fields, validate


class BaseSubscribeRequestSchema(Schema):
    card = fields.String(validate=validate.Length(max=20), required=True)
    name = fields.String(validate=validate.Length(max=20), required=False)
    email = fields.Email(required=False)
    tar_type_id = fields.Integer(required=True)
    active_date_from = fields.String(required=False)
    active_date_to = fields.String(required=False)

from schemas.base_subscription import BaseSubscribeRequestSchema
from marshmallow import fields, validate


class SubscribeResquestSchema(BaseSubscribeRequestSchema):
    pass


class SubscribeForEditSchema(BaseSubscribeRequestSchema):
    card = fields.String(validate=validate.Length(max=20), required=False)
    tar_type_id = fields.Integer(required=False)

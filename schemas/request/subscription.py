from schemas.base_subscription import BaseSubscribeResquestSchema
from marshmallow import fields, validate

class SubscribeResquestSchema(BaseSubscribeResquestSchema):
    pass

class SubscribeForEditSchema(BaseSubscribeResquestSchema):
    card = fields.String(validate=validate.Length(max=20), required=False)
    tar_type_id = fields.Integer(required=False)
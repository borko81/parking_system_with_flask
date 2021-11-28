from marshmallow import fields

from schemas.base_subscription import BaseSubscribeResquestSchema

class SubscribeResponseSchema(BaseSubscribeResquestSchema):
    id = fields.Integer()
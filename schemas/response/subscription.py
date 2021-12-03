from marshmallow import fields

from schemas.base_subscription import BaseSubscribeRequestSchema


class SubscribeResponseSchema(BaseSubscribeRequestSchema):
    id = fields.Integer()
    photo_url = fields.URL()

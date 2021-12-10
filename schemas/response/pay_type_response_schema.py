from marshmallow import fields

from schemas.pay_type_base_schema import PayTypeBaseSchema


class PayTypeResponseSchema(PayTypeBaseSchema):
    id = fields.Integer()

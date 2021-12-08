from schemas.pay_type_base_schema import PayTypeBaseSchema
from marshmallow import fields


class PayTypeResponseSchema(PayTypeBaseSchema):
    id = fields.Integer()

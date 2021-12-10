from marshmallow import Schema, fields

from schemas.response.pay_type_response_schema import PayTypeResponseSchema


class TransactionsSchema(Schema):
    id = fields.Integer()
    pr_id = fields.Integer()
    created_on = fields.DateTime()
    transaction_id = fields.Integer()
    pay_type = fields.Integer()
    payment_name = fields.Nested(PayTypeResponseSchema(only=("name",)))

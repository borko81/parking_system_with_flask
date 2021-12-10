from marshmallow import fields

from schemas.request.park_request_schema import ParkRequestSchema
from schemas.response.transaction_response_schema import TransactionsSchema


class ParkResponseSchema(ParkRequestSchema):
    id = fields.Integer()
    card = fields.String()
    income = fields.String()
    outcome = fields.String()
    price = fields.Number()
    pay = fields.Boolean()
    otc_id = fields.Integer()


class ParkResponseSchemaWithTransactions(ParkRequestSchema):
    id = fields.Integer()
    card = fields.String()
    income = fields.String()
    outcome = fields.String()
    price = fields.Number()
    pay = fields.Boolean()
    otc_id = fields.Integer()
    park_pay = fields.Nested(TransactionsSchema, many=True)

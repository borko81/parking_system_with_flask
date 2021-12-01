from marshmallow import fields

from schemas.request.park_request_schema import ParkRequestSchema


class ParkResponseSchema(ParkRequestSchema):
    id = fields.Integer()
    income = fields.String()
    outcome = fields.String()
    price = fields.Number()
    pay = fields.Boolean()
    otc_id = fields.Integer()

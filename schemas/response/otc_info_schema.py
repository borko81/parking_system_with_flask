from marshmallow import Schema, fields

from schemas.response.park_response_schema import (
    ParkResponseSchemaWithTransactions,
)


class OtcInfoSchema(Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    created_on = fields.DateTime()
    park_otc = fields.Nested(ParkResponseSchemaWithTransactions, many=True)

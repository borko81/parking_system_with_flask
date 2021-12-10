from marshmallow import Schema, fields

from schemas.response.park_response_schema import (
    ParkResponseSchemaWithTransactions,
)

"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user_model.id"), nullable=False)
    created_on = db.Column(db.DateTime, server_default=func.now())
    park_otc = db.relationship("ParkModel", backref="park_otc", lazy="dynamic")
"""


class OtcInfoSchema(Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    created_on = fields.DateTime()
    park_otc = fields.Nested(ParkResponseSchemaWithTransactions, many=True)

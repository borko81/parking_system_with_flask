from marshmallow import Schema, fields
from schemas.response.pay_type_response_schema import PayTypeResponseSchema

"""
    id = db.Column(db.Integer, primary_key=True)
    pr_id = db.Column(db.Integer, db.ForeignKey('park.id'), nullable=False)
    created_on = db.Column(db.DateTime, server_default=func.now())
    transaction_id = db.Column(db.Integer, nullable=False, default=None)
    pay_type = db.Column(db.Integer, db.ForeignKey('pay_type.id'), nullable=False)
    pay_type_relationship = db.relationship('PayType', backref='pay_type_relationship', lazy='dynamic')
"""


class TransactionsSchema(Schema):
    id = fields.Integer()
    pr_id = fields.Integer()
    created_on = fields.DateTime()
    transaction_id = fields.Integer()
    pay_type = fields.Integer()
    payment_name = fields.Nested(PayTypeResponseSchema(only=("name",)))

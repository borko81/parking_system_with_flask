from marshmallow import Schema, fields


class ParkEnterSchema(Schema):
    card = fields.String(required=True)


class ParkResponseSchema(ParkEnterSchema):
    id = fields.Integer()
    income = fields.String()


class ParkWhoAlreadyOut(ParkResponseSchema):
    outcome = fields.String()
    tarif_id = fields.String()
    pay = fields.Boolean()

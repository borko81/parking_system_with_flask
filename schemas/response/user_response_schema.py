from marshmallow import fields, Schema
from schemas.request.user_request_schema import UserRegisterSchema


class UserResponceSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    type = fields.String()

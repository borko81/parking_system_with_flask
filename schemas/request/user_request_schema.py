from marshmallow import Schema, fields, validate, ValidationError
from password_strength import PasswordPolicy
from decouple import config

policy = PasswordPolicy.from_names(uppercase=1, numbers=1)


def validate_password(value):
    """
    Validate if password is ok or not use policy
    :param value:
    :return raise when invalid
    """
    errors = policy.test(value)
    if errors:
        raise ValidationError("Not valid password try again")


def validate_name(value):
    if len(value.split()) < 3:
        raise ValidationError("Username must have three name")


class UserRegisterSchema(Schema):
    name = fields.String(
        required=True,
        validate=validate.And(
            validate.Length(max=config("USER_NAME_FIELD_LENGTH", cast=int)),
            validate_name,
        ),
    )
    password = fields.String(
        required=True,
        validate=validate.And(
            validate.Length(max=config("USER_PASSWORD_FIELD_LENGTH", cast=int)),
            validate_password,
        ),
    )
    type = fields.String(required=False)


class UserEditSchema(UserRegisterSchema):
    pass

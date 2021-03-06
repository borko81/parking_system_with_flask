import re
from functools import wraps

from flask import request
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest, Forbidden

from managers.auth import auth


def validate_schema(schema_name):
    def decorator(f):
        @wraps(f)
        def docorated_func(*args, **kwargs):
            schema = schema_name()
            errors = schema.validate(request.get_json())
            if errors:
                raise BadRequest(f"Invalid fields {errors}")
            return f(*args, **kwargs)

        return docorated_func

    return decorator


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = auth.current_user()
            if not str(user.type) == str(permission):
                raise Forbidden("You do not have the rights to access this resource")
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def validate_stay(value):
    if re.match("\d{2}:\d{2}", value) is None:
        raise ValidationError("Not valid field! Expect something like 01:01")

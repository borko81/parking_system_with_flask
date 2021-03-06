from sqlalchemy.types import TypeDecorator

from db import db


class StrippedString(TypeDecorator):
    """
    Use to check unique name is stay uniq
    even in lowercase and uppercase letters insert.
    """

    impl = db.String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return value.strip() if value else value

    def copy(self, **kw):
        return StrippedString(self.impl.length)

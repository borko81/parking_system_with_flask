from sqlalchemy.types import TypeDecorator

from db import db


class StrippedString(TypeDecorator):
    impl = db.String

    def process_bind_param(self, value, dialect):
        return value.strip() if value else value

    def copy(self, **kw):
        return StrippedString(self.impl.length)

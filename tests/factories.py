from db import db
from random import randint

import factory

from models import UserModel
from models.enum import UserType


class BaseFactory(factory.Factory):
    @classmethod
    def create(cls, **kwargs):
        object = super().create(**kwargs)
        db.session.add(object)
        db.session.flush()
        return object


class AdminUserFactory(BaseFactory):
    class Meta:
        model = UserModel

    id = factory.Sequence(lambda n: n)
    name = "Admin Admin Admin"
    password = 'A123'
    type = UserType.admin


class StaffUserFactory(BaseFactory):
    class Meta:
        model = UserModel

    id = factory.Sequence(lambda n: n)
    name = "Staff1 Staff Staff"
    password = 'A123'
    type = UserType.staff
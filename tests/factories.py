import factory

from db import db
from models import UserModel, TariffTypeModel
from models.enum import UserType
from models.subscription import SubscriptionModel


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

    id = factory.Sequence(lambda n: n + 1)
    name = "Admin Admin Admin"
    password = "A123"
    type = UserType.admin


class StaffUserFactory(BaseFactory):
    class Meta:
        model = UserModel

    id = factory.Sequence(lambda n: n + 1)
    name = "Staff Staff Staff"
    password = "A123"
    type = UserType.staff


class SubscribeFactory(BaseFactory):
    class Meta:
        model = SubscriptionModel

    id = factory.Sequence(lambda n: n + 1)
    card = "A111"
    email = "A111@abv.bg"
    tar_type_id = 1

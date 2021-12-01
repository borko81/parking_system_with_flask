from werkzeug.exceptions import BadRequest, NotFound

from db import db
from models.subscription import SubscriptionModel


class SubscribeManager:
    @staticmethod
    def insert_new(data):
        """
        First validate card already exists in table if true, raise Error, else insert it.
        :param data:
        :return:
        """
        if SubscriptionModel.get_from_card(data["card"]).first():
            raise BadRequest("Card already exists")
        insert_in_model = SubscriptionModel(**data)
        db.session.add(insert_in_model)
        db.session.flush()
        return {
            "message": "Successfully added card with id {}".format(insert_in_model.id)
        }

    @staticmethod
    def get_subscriptions():
        return SubscriptionModel.query.all()


class SubsribeConcretManager:
    @staticmethod
    def get_sub(_id):
        sub = SubscriptionModel.query.filter_by(id=_id)
        if sub.first():
            return sub
        raise NotFound("Invalid id {}".format(_id))

    @staticmethod
    def edit_sub(_id: int, data):
        sub = SubsribeConcretManager.get_sub(_id)
        sub.update(data)
        db.session.flush()
        return sub

    @staticmethod
    def delete_sub(_id):
        sub = SubsribeConcretManager.get_sub(_id)
        db.session.delete(sub.first())
        return 204


class SubscribeShowFromTypeManager:
    @staticmethod
    def get_all_from_type(_id):
        check = SubscriptionModel.get_from_type(_id)
        return check

from werkzeug.exceptions import NotFound

from db import db
from helpers.data_preparation import data_preparate_for_commit
from models.pay_type import PayType
from schemas.response.pay_type_response_schema import PayTypeResponseSchema


class PayTypeManager:
    @staticmethod
    def get_all():
        data = PayType.query.all()
        schema = PayTypeResponseSchema()
        return schema.dump(data, many=True)

    @staticmethod
    def insert_new(data):
        new_pay_type = PayType(**data)
        data_preparate_for_commit(new_pay_type)
        schema = PayTypeResponseSchema()
        return schema.dump(new_pay_type)


class PayTypeIDManager:
    @staticmethod
    def get(_id):
        data = PayType.query.filter_by(id=_id)
        if not data.first():
            raise NotFound("Not found id: {}".format(_id))
        return data

    @staticmethod
    def delete(_id):
        pay_type = PayTypeIDManager.get(_id)
        db.session.delete(pay_type.first())
        return 204

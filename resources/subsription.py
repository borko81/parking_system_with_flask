from flask import request
from flask_restful import Resource

from helpers.decorator import validate_schema
from managers.subscription_manager import (
    SubscribeManager,
    SubsribeConcretManager,
    SubscribeShowFromTypeManager,
)
from schemas.request.subscription import SubscribeResquestSchema, SubscribeForEditSchema
from schemas.response.subscription import SubscribeResponseSchema


class SubscriptionRes(Resource):
    @staticmethod
    def get():
        """
        usage: curl 127.0.0.1:5000/subscription
        """
        result = SubscribeManager.get_subscriptions()
        schema = SubscribeResponseSchema()
        return schema.dump(result, many=True)

    @validate_schema(SubscribeResquestSchema)
    def post(self):
        """
        usage: curl 127.0.0.1:5000/subscription -X POST -H "Content-type:application/json" -d
                                                '{"card": "1234", "email":"test@abv.bg", "tar_type_id": 2}'
        """
        data = request.get_json()
        result = SubscribeManager.insert_new(data)
        return {"message": result}, 201


class SubscribeFromIdRes(Resource):
    @staticmethod
    def get(_id):
        """
        usage:  curl 127.0.0.1:5000/subscription/14
        :param _id: int
        :return: json when id found else massage invalid id
        """
        res = SubsribeConcretManager.get_sub(_id)
        schema = SubscribeResponseSchema()
        return schema.dump(res.first())

    @validate_schema(SubscribeForEditSchema)
    def put(self, _id):
        """
        usage: curl 127.0.0.1:5000/subscription/2 -X PUT -H "Content-type:application/json" -d
                                                    '{"card": "4321", "tar_type_id": 2, "all": "test"}'
        """
        data = request.get_json()
        schema = SubscribeResponseSchema()
        res = SubsribeConcretManager.edit_sub(_id, data)
        return schema.dump(res.first())

    @staticmethod
    def delete(_id):
        """
        usage: curl 127.0.0.1:5000/subscription/21 -X DELETE
        """
        return SubsribeConcretManager.delete_sub(_id)


class SubscriptionFromType(Resource):
    @staticmethod
    def get(_id):
        """
        usage: curl 127.0.0.1:5000/subscription/type/2
        """
        schema = SubscribeResponseSchema()
        model_result = SubscribeShowFromTypeManager.get_all_from_type(_id)
        return schema.dump(model_result, many=True)

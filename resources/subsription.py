from flask import request
from flask_restful import Resource

from helpers.decorator import validate_schema
from managers.auth import auth
from managers.subscription_manager import (
    SubscribeManager,
    SubsribeConcretManager,
    SubscribeShowFromTypeManager,
)
from schemas.request.subscription import SubscribeResquestSchema, SubscribeForEditSchema
from schemas.response.subscription import SubscribeResponseSchema


class SubscriptionRes(Resource):
    @staticmethod
    @auth.login_required
    def get():
        """
        Return all card subscribe
        ---
        tags:
        - Card
        parameters:
        - name: Authorization
          in: header
        responses:
          200:
            description: Ok
          401:
            description: Unauthorized
        """
        result = SubscribeManager.get_subscriptions()
        schema = SubscribeResponseSchema()
        return schema.dump(result, many=True)

    @validate_schema(SubscribeResquestSchema)
    @auth.login_required
    def post(self):
        """
        Insert new card
        ---
        tags:
        - Card
        parameters:
        - name: Authorization
          in: header
        - name: data
          in: body
        responses:
          201:
            description: Success
          401:
            description: Unauthorized
          400:
            description: Bad Request, found duplicate
        """
        data = request.get_json()
        result = SubscribeManager.insert_new(data)
        return {"message": result}, 201


class SubscribeFromIdRes(Resource):
    @staticmethod
    @auth.login_required
    def get(_id):
        """
        Return card from given id
        ---
        tags:
        - Card
        parameters:
        - name: Authorization
          in: header
        - name: _id
          in: path
        responses:
          200:
            description: Ok
          401:
            description: Not Found
        """
        res = SubsribeConcretManager.get_sub(_id)
        schema = SubscribeResponseSchema()
        return schema.dump(res.first())

    @validate_schema(SubscribeForEditSchema)
    @auth.login_required
    def put(self, _id):
        """
        Edit new card if found
        ---
        tags:
        - Card
        parameters:
        - name: Authorization
          in: header
        - name: _id
          in: path
        - name: data
          in: body
        responses:
          200:
            description: OK
          401:
            description: Unauthorized
          404:
            description: Bad Request, found duplicate
        """
        data = request.get_json()
        schema = SubscribeResponseSchema()
        res = SubsribeConcretManager.edit_sub(_id, data)
        return schema.dump(res.first())

    @staticmethod
    @auth.login_required
    def delete(_id):
        """
        Delete card if found card with that id, else retrun Not found
        ---
        tags:
        - Card
        parameters:
        - name: Authorization
          in: header
        - name: _id
          in: path
        responses:
          200:
            description: Ok
          401:
            description: Unauthorized
          404:
            description: Not found
        """
        return SubsribeConcretManager.delete_sub(_id)


class SubscriptionFromType(Resource):
    @staticmethod
    def get(_type):
        """
        Return cards from givent type
        ---
        tags:
        - Card
        parameters:
        - name: Authorization
          in: header
        - name: _type
          in: path
        responses:
          200:
            description: Ok
          401:
            description: Unauthorized
          404:
            description: Not found
        """
        schema = SubscribeResponseSchema()
        model_result = SubscribeShowFromTypeManager.get_all_from_type(_type)
        return schema.dump(model_result, many=True)

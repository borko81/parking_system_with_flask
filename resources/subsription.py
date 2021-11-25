from flask_restful import Resource


class SubscriptionRes(Resource):
    def get(self):
        "Return all subscriptions"
        pass

    def post(self):
        pass


class SubsciprConcretRes(Resource):
    def get(self, _id):
        "Return concret subscription info"
        pass

    def put(self, _id):
        pass

    def delete(self, _id):
        pass


class SubscriptionFromType(Resource):
    def get(self, type):
        "Return subscription generate by concret type"
        pass

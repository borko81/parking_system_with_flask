from flask_restful import Resource


class ParkingRes(Resource):
    def get(self):
        "Show all car in parking who is not payed yet"
        pass

    def post(self):
        """Here is a too big black magic"""
        pass


class ParkingTetailInfoRes(Resource):
    """Only from admin"""
    def get(self, _id):
        pass

    def put(self, _id):
        pass

    def delete(self, _id):
        pass


class ParkingPayRes(Resource):
    def post(self):
        pass


class ParkingAlreadyPay(Resource):
    def get(self):
        pass

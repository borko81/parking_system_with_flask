from flask_restful import Resource
from managers.pay_manager import PayWiseManager, PayCashManager
from resources.parking import ParkingDetailInfoRes

mapper = {
    "wise": lambda x: PayWiseManager.new_pay(x),
    "cash": lambda x: PayCashManager.new_pay(x),
}


class PayResourse(Resource):
    def post(self, _id, pay):
        result = mapper[pay](_id)
        return result

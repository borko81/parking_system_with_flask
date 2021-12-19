from flask_restful import Resource

from managers.auth import auth
from managers.pay_manager import PayWiseManager, PayCashManager

mapper = {
    "wise": lambda x: PayWiseManager.new_pay(x),
    "cash": lambda x: PayCashManager.new_pay(x),
}


class PayResourse(Resource):
    @auth.login_required
    def post(self, _id, pay):
        result = mapper[pay](_id)
        return result

from flask_restful import Resource

from managers.auth import auth
from managers.get_payed_bills_and_close_in_otc import (
    GenerateOTCManager,
    GetDetailForOtcManager,
)


class GenerateOtcResourse(Resource):
    @auth.login_required
    def post(self):
        return GenerateOTCManager.close_bill_to_otc()


class ShowOtcDetail(Resource):
    @staticmethod
    @auth.login_required
    def get(_id):
        return GetDetailForOtcManager.get_otc_from_id(_id)

from werkzeug.exceptions import BadRequest, NotFound

from helpers.data_preparation import data_preparate_for_commit
from managers.auth import auth
from models.otc_model import OtcModel
from models.park import ParkModel
from schemas.response.otc_info_schema import OtcInfoSchema


class GenerateOTCManager:
    @staticmethod
    def get_all_payed_bill_who_not_have_otc_id():
        return [
            p
            for p in ParkModel.query.filter(
                (ParkModel.pay == True) & (ParkModel.otc_id == None)
            )
        ]

    @staticmethod
    def insert_new_otc_id():
        """TODO Generate zero otc !!!, this is question to do or not"""
        user = auth.current_user()
        otc_id = OtcModel(user_id=user.id)
        data_preparate_for_commit(otc_id)
        return otc_id.id

    @staticmethod
    def close_bill_to_otc():
        otc_id = GenerateOTCManager.insert_new_otc_id()
        try:
            for r in GenerateOTCManager.get_all_payed_bill_who_not_have_otc_id():
                r.otc_id = otc_id
        except:
            raise BadRequest("Unexpected problem acquire")
        return {"message": "Success", "otc_id": otc_id}


class GetDetailForOtcManager:
    @staticmethod
    def get_otc_from_id(_id):
        otc = OtcModel.query.filter_by(id=_id)
        if otc.first():
            schema = OtcInfoSchema()
            return schema.dump(otc.first())
        raise NotFound("Not found otc with that id: {}".format(_id))

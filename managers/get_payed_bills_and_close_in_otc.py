import json

from flask_restful import abort
from werkzeug.exceptions import BadRequest, NotFound

from helpers.data_preparation import data_preparate_for_commit
from helpers.loger_config import custom_logger
from managers.auth import auth
from models import Transaction, UserModel
from models.otc_model import OtcModel
from models.park import ParkModel
from schemas.response.otc_info_schema import OtcInfoSchema
from services.send_email_with_gmail import send_email_notification


def get_sum_for_otc_send_email(_id):
    analysis_data = OtcModel.query.filter_by(id=_id).first()
    data = {
        "Data For": str(analysis_data.created_on),
        "User": UserModel.find_from_id(analysis_data.user_id).first().name,
        "Cash": sum(
            [
                float(i.price)
                for i in analysis_data.park_otc
                if Transaction.query.filter_by(pr_id=i.id).first().pay_type == 1
            ]
        ),
        "Wise": sum(
            [
                float(i.price)
                for i in analysis_data.park_otc
                if Transaction.query.filter_by(pr_id=i.id).first().pay_type == 2
            ]
        ),
    }
    try:
        send_email_notification(json.dumps(data))
        custom_logger("info", "Successfully send email with otc data")
    except Exception:
        abort(400)


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
        try:
            get_sum_for_otc_send_email(otc_id)
        except Exception:
            pass
        finally:
            return {"message": "Success", "otc_id": otc_id}


class GetDetailForOtcManager:
    @staticmethod
    def get_otc_from_id(_id):
        otc = OtcModel.query.filter_by(id=_id)
        if otc.first():
            schema = OtcInfoSchema()
            return schema.dump(otc.first())
        raise NotFound("Not found otc with that id: {}".format(_id))

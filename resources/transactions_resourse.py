from flask import request
from flask_restful import Resource

from managers.transactions_manager import TransactionsManager, TransactionsInfoManager
from managers.auth import auth
from helpers.decorator import permission_required
from models.enum import UserType


class TransactionsResourse(Resource):
    @auth.login_required
    @permission_required(UserType.admin)
    def get(self):
        return TransactionsManager.get_all()


class TransactionInfoResourse(Resource):
    @auth.login_required
    @permission_required(UserType.admin)
    def get(self):
        _id = request.args.get("id", None)
        _tr_id = request.args.get("trans_id", None)
        return TransactionsInfoManager.get_from_id(_id, _tr_id)

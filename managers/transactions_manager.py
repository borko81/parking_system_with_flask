from models.payment_transaction import Transaction
from schemas.response.transaction_response_schema import TransactionsSchema


class TransactionsManager:
    @staticmethod
    def get_all():
        schema = TransactionsSchema()
        data = Transaction.query.all()
        return schema.dump(data, many=True)


class TransactionsInfoManager:
    @staticmethod
    def get_from_id(_id, _tr_id):
        schema = TransactionsSchema()
        data = Transaction.query.filter(
            (Transaction.id == _id) | (Transaction.transaction_id == _tr_id)
        ).first()
        return schema.dump(data)

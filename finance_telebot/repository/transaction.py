from datetime import datetime
from typing import List

from bson.objectid import ObjectId

from finance_telebot.entity import Transaction


class TransactionError(Exception):
    pass


class TransationFilter:
    def __init__(self):
        self.a = ''
        self.b = ''


class TransactionRepository:
    col_name = 'transactions'

    def __init__(self, db: dict):
        self._table = db[self.col_name]

    def get(self, tid: str) -> Transaction:
        trx = self._table.find_one({'_id': tid})
        if not trx:
            raise TransactionError('Transaction not found')
        tr = Transaction.from_json(trx)
        return tr

    def find(self, filter: TransationFilter) -> List[Transaction]:
        return [Transaction.from_json({})]

    def save(self, trx: Transaction):
        now = datetime.now()
        trx.id = str(ObjectId())
        trx.created_at = now
        trx.updated_at = now
        try:
            self._table.insert_one(trx.as_json)
        except Exception as e:
            raise TransactionError(e)

    def update(self, trx: Transaction):
        now = datetime.now()
        trx.updated_at = now
        try:
            res = self._table.update_one(
                {'_id': trx.id},
                {'$set': trx.as_json}
            )
        except Exception as e:
            raise TransactionError(e)

        if res.modified_count != 1:
            raise TransactionError('Transaction not updated')

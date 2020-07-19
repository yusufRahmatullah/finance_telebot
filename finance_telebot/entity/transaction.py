import re
from datetime import date, datetime

from finance_telebot.entity.period import Period


class Transaction:
    def __init__(self, date: date, category: str, amount: int, wallet: str,
                 notes: str = '', period: Period = None):
        now = datetime.now()
        self.id = ''
        self.date = date
        self.category = category
        self.amount = amount
        self.wallet = wallet
        self.notes = notes
        if period:
            self.period = period
        else:
            self.period = Period.now()
        self.created_at = now
        self.updated_at = now

    def __str__(self) -> str:
        d = self.date
        c = self.category
        a = self.format_amount()
        w = self.wallet
        n = self.wallet
        return f'{d} - {c} - {a} - {w} - {n}'

    @property
    def as_json(self) -> dict:
        return {
            'id': self.id,
            'date': self.date,
            'category': self.category,
            'amount': self.amount,
            'wallet': self.wallet,
            'notes': self.notes,
            'period': str(self.period),
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def format_amount(self) -> str:
        orig = str(self.amount)
        new = re.sub(r"^(-?\d+)(\d{3})", r"\g<1>.\g<2>", orig)
        left_part = new.partition('.')[0]
        while len(left_part) > 3:
            new = re.sub(r"^(-?\d+)(\d{3})", r"\g<1>.\g<2>", new)
            left_part = new.partition('.')[0]
        return new

    @classmethod
    def from_json(cls, data: dict) -> 'Transaction':
        period = Period.parse(data.get('period'))
        trx = Transaction(
            data['date'], data['category'], data['amount'], data['wallet'],
            notes=data.get('notes', ''), period=period
        )
        trx.id = data['_id']
        trx.created_at = data['created_at']
        trx.updated_at = data['updated_at']
        return trx

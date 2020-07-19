from finance_telebot.entity import Transaction
from finance_telebot.repository import TransactionRepository
from finance_telebot.util import Logger


class TransactionUseCase:
    def __init__(self, repo: TransactionRepository):
        self.repo = repo

    def create_transaction(self, words: list) -> str:
        # trx = Transaction(date, category, amount, wallet, notes, period)
        return ''

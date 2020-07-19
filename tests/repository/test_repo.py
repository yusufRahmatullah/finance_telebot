from datetime import datetime
from unittest.mock import Mock

from finance_telebot.entity import Period, Transaction
from finance_telebot.repository import TransactionRepository
from finance_telebot.repository.transaction import TransactionError

import pytest

from tests.repository.util import ResMock

now = datetime.now()
table = Mock()
db = {TransactionRepository.col_name: table}
repo = TransactionRepository(db)


def test_get():
    period = Period.now()
    table.find_one.return_value = {
        '_id': '1',
        'date': now.date(),
        'category': 'Makan',
        'amount': 1_000,
        'wallet': 'Jenius',
        'period': str(period),
        'notes': 'testing',
        'created_at': now,
        'updated_at': now
    }

    trx = repo.get('1')
    assert trx.id == '1'
    assert trx.date == now.date()
    assert trx.category == 'Makan'
    assert trx.amount == 1_000
    assert trx.wallet == 'Jenius'
    assert str(trx.period) == str(period)
    assert trx.notes == 'testing'
    assert trx.created_at == now
    assert trx.updated_at == now


def test_get_empty():
    table.find_one.return_value = None
    with pytest.raises(TransactionError):
        repo.get('1')


def test_save():
    table.insert_one.return_value = ResMock(ack=True)
    trx = Transaction(now.date(), 'Makan', 1_000, 'Jenius')
    repo.save(trx)

    assert trx.id
    assert trx.created_at
    assert trx.created_at == trx.updated_at


def test_save_error():
    table.insert_one.side_effect = Exception()
    trx = Transaction(now.date(), 'Makan', 1_000, 'Jenius')
    with pytest.raises(TransactionError):
        repo.save(trx)


def test_update():
    table.update_one.return_value = ResMock(modified_count=1)
    trx = Transaction(now.date(), 'Makan', 1_000, 'Jenius')
    trx.created_at = now
    trx.updated_at = now
    repo.update(trx)

    assert trx.updated_at > trx.created_at


def test_update_failed():
    table.update_one.return_value = ResMock(modified_count=0)
    trx = Transaction(now.date(), 'Makan', 1_000, 'Jenius')
    with pytest.raises(TransactionError):
        repo.update(trx)

    table.update_one.side_effect = Exception()
    with pytest.raises(TransactionError):
        repo.update(trx)

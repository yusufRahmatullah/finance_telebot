from finance_telebot.entity import category
from finance_telebot.util import Logger

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler


class BaseCallback:
    def __init__(self, logger: Logger):
        self.logger = logger

    def perform(self, update, context):
        raise NotImplementedError


class CallbackHandler:
    def __init__(self, logger: Logger):
        self.logger = logger
        self.handler = CallbackQueryHandler(self._perform)
        self.callbacks = {}

    def _perform(self, update, context):
        chat_id = update.effective_chat.id
        username = update.effective_user.username
        data = update.callback_query.data
        command, _, words = data.partition(' ')
        self.logger.info(
            f'Get callback from {username} on chat {chat_id}: {command} - {words}'
        )
        cb = self.callbacks[command]
        context.user_data[cb.name] = words
        cb.perform(update, context)

    def add_callback(self, callback: BaseCallback):
        self.callbacks[callback.name] = callback

    def register(self, dispatcher):
        dispatcher.add_handler(self.handler)


class TransactionCategoryCallback(BaseCallback):
    name = 'transaction-category'    

    def __init__(self, logger: Logger):
        super().__init__(logger)
        self._init_wallet_buttons()

    def _init_wallet_buttons(self):
        self.wallet_buttons = []
        wals = list(category.wallets)
        for wal1, wal2 in zip(wals[0::2], wals[1::2]):
            btn1 = InlineKeyboardButton(
                text=wal1,
                callback_data=f'transaction-wallet {wal1}'
            )
            btn2 = InlineKeyboardButton(
                text=wal2,
                callback_data=f'transaction-wallet {wal2}'
            )
            self.wallet_buttons.append([btn1, btn2])

    def perform(self, update, context):
        chat_id = update.effective_chat.id
        username = update.effective_user.username
        cat = context.user_data[self.name]
        self.logger.info(
            f'Category choosen by {username} on chat {chat_id}: {cat}'
        )
        context.bot.send_message(
            chat_id=chat_id,
            text='Silahkan memilih wallet',
            reply_markup=InlineKeyboardMarkup(self.wallet_buttons)
        )


class TransactionWalletCallback(BaseCallback):
    name = 'transaction-wallet'

    def perform(self, update, context):
        chat_id = update.effective_chat.id
        username = update.effective_user.username
        cat = context.user_data[TransactionCategoryCallback.name]
        wal = context.user_data[self.name]
        self.logger.info(
            f'Wallet choosen by {username} on chat {chat_id}: {wal}'
        )
        context.bot.send_message(
            chat_id=chat_id,
            text=f'Kamu memilih kategori "{cat}" dan wallet "{wal}"'
        )
        context.bot.send_message(
            chat_id=chat_id,
            text='Silahkan masukkan amount'
        )

from finance_telebot.entity import category
from finance_telebot.util import Logger

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler


class BaseCommand:
    def __init__(self, name: str, logger: Logger):
        self.name = name
        self.handler = CommandHandler(name, self._perform)
        self.logger = logger

    def _perform(self, update, context):
        chat_id = update.effective_chat.id
        username = update.effective_user.username
        text = update.effective_message.text
        self.logger.info(
            f'Get message from {username} on chat {chat_id}: {text}'
        )
        response = self.response(context.args)
        self.logger.info(
            f'Respond {username} on chat {chat_id}: {response}'
        )
        context.bot.send_message(
            chat_id=chat_id,
            text=response
        )

    def register(self, dispatcher):
        dispatcher.add_handler(self.handler)

    def response(self, args: list) -> str:
        raise NotImplementedError


class StartCommand(BaseCommand):
    def __init__(self, logger: Logger):
        super().__init__('start', logger)

    def response(self, args: list) -> str:
        return 'Hi, Selamat Datang di Finance Bot'


class TransactionCommand(BaseCommand):
    def __init__(self, logger: Logger):
        super().__init__('transaction', logger)
        self._init_category_buttons()
        
    def _init_category_buttons(self):
        self.category_buttons = []
        cats = list(category.categories)
        for cat1, cat2 in zip(cats[0::2], cats[1::2]):
            btn1 = InlineKeyboardButton(
                text=cat1,
                callback_data=f'transaction-category {cat1}'
            )
            btn2 = InlineKeyboardButton(
                text=cat2,
                callback_data=f'transaction-category {cat2}'
            )
            self.category_buttons.append([btn1, btn2])

    def _perform(self, update, context):
        chat_id = update.effective_chat.id
        username = update.effective_user.username
        text = update.effective_message.text
        self.logger.info(
            f'Get message from {username} on chat {chat_id}: {text}'
        )
        context.bot.send_message(
            chat_id=chat_id,
            text='Silahkan pilih kategorinya',
            reply_markup=InlineKeyboardMarkup(self.category_buttons)
        )

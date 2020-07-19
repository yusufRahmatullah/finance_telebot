import os

from callback import (
    CallbackHandler,
    TransactionCategoryCallback,
    TransactionWalletCallback
)

from command import StartCommand, TransactionCommand

from finance_telebot.util import Logger

from telegram.ext import Updater, MessageHandler
from telegram.ext.filters import Filters


def _init_commands(dispatcher, logger):
    start_command = StartCommand(logger)
    start_command.register(dispatcher)

    trx_command = TransactionCommand(logger)
    trx_command.register(dispatcher)


def _init_callbacks(dispatcher, logger):
    callback_handler = CallbackHandler(logger)
    callback_handler.register(dispatcher)

    trx_cat_cb = TransactionCategoryCallback(logger)
    callback_handler.add_callback(trx_cat_cb)

    trx_wal_cb = TransactionWalletCallback(logger)
    callback_handler.add_callback(trx_wal_cb)


def err_handler(update, context):
    print('Error occurred:', context.error)


def run(updater: Updater, token: str):
    mode = os.getenv('MODE')
    if mode == 'dev':
        updater.start_polling()
    elif mode == 'prod':
        app_name = os.getenv('HEROKU_APP_NAME')
        port = int(os.getenv('PORT', '8443'))
        updater.start_webhook(
            listen='0.0.0.0',
            port=port,
            url_path=token
        )
        updater.bot.set_webhook(
            f'https://{app_name}.herokuapp.com/{token}'
        )


def number_handler(update, context):
    chat_id = update.effective_chat.id
    username = update.effective_user.username
    cat = context.user_data.get(TransactionCategoryCallback.name)
    wal = context.user_data.get(TransactionWalletCallback.name)
    amount = int(update.effective_message.text)
    if cat and wal:
        context.user_data['transaction-amount'] = amount
        context.bot.send_message(
            chat_id=chat_id,
            text=f'Kamu memasukkan amount sebesar {amount}'
        )
        context.bot.send_message(
            chat_id=chat_id,
            text='Silahkan masukkan notes'
        )    


def text_handler(update, context):
    chat_id = update.effective_chat.id
    username = update.effective_user.username
    cat = context.user_data.get(TransactionCategoryCallback.name)
    wal = context.user_data.get(TransactionWalletCallback.name)
    amount = context.user_data['transaction-amount']
    notes = update.effective_message.text
    if cat and wal and amount:
        context.bot.send_message(
            chat_id=chat_id,
            text=f'Kamu memasukkan notes: "{notes}"'
        )
        context.bot.send_message(
            chat_id=chat_id,
            text=(
                f'Kamu akan memasukkan transaksi dengan kategori "{cat}" '
                f'dengan wallet "{wal}" sebesar Rp{amount} '
                f'untuk keperluan "{notes}"'
            )
        )


def main():
    logger = Logger('finance_telebot.log', os.getenv('DEBUG') == 'true')
    logger.info('Starting Finance Bot')
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    updater = Updater(
        token=os.getenv('TELEGRAM_BOT_TOKEN'),
        use_context=True
    )
    dispatcher = updater.dispatcher
    _init_commands(dispatcher, logger)
    _init_callbacks(dispatcher, logger)
    dispatcher.add_handler(MessageHandler(
        Filters.regex(r'^(\d+)$'),
        number_handler
    ))
    dispatcher.add_handler(MessageHandler(
        Filters.text, text_handler
    ))
    
    # register_dispatcher(dispatcher)
    # jq = updater.job_queue
    # jq.run_repeating(command.job_save_mem, 3 * 3600, 3600)
    run(updater, token)
    updater.idle()
    logger.info('Stopping Finance Bot')
    updater.stop()


if __name__ == '__main__':
    main()

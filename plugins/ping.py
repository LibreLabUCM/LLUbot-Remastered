from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async

class Plugin:
    def __init__(self, main, updater):
        self.main = main
        self.updater = updater
        self.logger = main.logger
        updater.dispatcher.add_handler(CommandHandler('ping', self.ping))
        updater.dispatcher.add_handler(CommandHandler('noping', self.noping))

    @run_async
    def ping(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Pong")

    @run_async
    def noping(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="No Pong")

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async

class Plugin:
    def __init__(self, main, updater):
        self.main = main
        self.updater = updater
        self.logger = main.logger
        updater.dispatcher.add_handler(CommandHandler('help', self.help))

    @run_async
    def help(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Help")

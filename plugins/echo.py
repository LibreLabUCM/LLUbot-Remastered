from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async

class Plugin:
    def __init__(self, main, updater):
        self.main = main
        self.updater = updater
        self.logger = main.logger
        updater.dispatcher.add_handler(CommandHandler('echo', self.echo))

    @run_async
    def echo(self, bot, update):
        update.message.reply_text(update.message.text)

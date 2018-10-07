from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async

class Plugin:
    def __init__(self, main, updater):
        updater.dispatcher.add_handler(CommandHandler('echo', self.echo))

    @run_async
    def echo(self, bot, update):
        update.message.reply_text(update.message.text)

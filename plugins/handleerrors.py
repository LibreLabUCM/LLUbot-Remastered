from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async

class Plugin:
    def __init__(self, main, updater):
        self.main = main
        self.updater = updater
        self.logger = main.logger
        updater.dispatcher.add_handler(CommandHandler('echo', self.echo))
        updater.dispatcher.add_error_handler(self.onerror)

    @run_async
    def onerror(self, bot, update, error):
        logger.warning('Update "%s" caused error "%s"', update, error)

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async

class Plugin:
    def __init__(self, main, updater):
        self.logger = main.logger
        updater.dispatcher.add_handler(MessageHandler(Filters.text, self.noncommand))

    @run_async
    def noncommand(self, bot, update):
        self.logger.info('[%s] %s', update.message.from_user.first_name, update.message.text)
        update.message.reply_text("Not a command: %s" % update.message.text)

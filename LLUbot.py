from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async

import configparser
import logging

defaultExampleToken = '123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11'

logger = logging.getLogger(__name__)

@run_async
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hi")

@run_async
def help(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="/ping")

@run_async
def ping(bot, update):
    update.message.reply_text("Pong")

@run_async
def echo(bot, update):
    update.message.reply_text(update.message.text)

@run_async
def noncommand(bot, update):
    logger.info('[%s] %s', update.message.from_user.first_name, update.message.text)
    update.message.reply_text("Not a command: %s" % update.message.text)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    token = config.get('BotConfig', 'token', fallback=defaultExampleToken)
    workers = int(config.getint('BotConfig', 'workers', fallback=4))
    
    handlers = []
    handlers.append(logging.FileHandler('LLUbot.log'))
    handlers.append(logging.StreamHandler())
    datefmt="%Y-%m-%d %H:%M:%S"
    logging.basicConfig(format='[%(asctime)s][%(levelname)s] %(message)s', level=logging.INFO, datefmt=datefmt, handlers = handlers)
    logger = logging.getLogger(__name__)
    
    logger.info('Configured %i workers', workers)

    assert token != defaultExampleToken, "Set a token in the configuration file"
    
    updater = Updater(token=token, workers=workers)
    bot = updater.bot
    dispatcher = updater.dispatcher

    logger.info('Bot started')
    
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('ping', ping))
    dispatcher.add_handler(CommandHandler('echo', echo))
    dispatcher.add_handler(MessageHandler(Filters.text, noncommand))
    
    dispatcher.add_error_handler(error)

    botinfo = bot.get_me()
    logger.info('Bot: @%s (%s)', botinfo.username, botinfo.first_name)


    updater.start_polling()
    logger.info('Bot ready')
    updater.idle()
    logger.info('Bot stopped')


if __name__ == '__main__':
    main()

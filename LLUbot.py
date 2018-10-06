from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async

import configparser
import logging

import importlib
import pkgutil


defaultExampleToken = '123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11'


class LLUbot:
    def __init__(self, configFileName):
        self.configFileName = configFileName
        self.loadconfig()
        self.setupLogger()

        self.logger.info('Configured %i workers', self.workers)

        # Setup Bot
        assert self.token != defaultExampleToken, "Set a token in the configuration file"
        self.updater = Updater(token=self.token, workers=self.workers)
        self.bot = self.updater.bot
        self.dispatcher = self.updater.dispatcher
        self.logger.info('Bot started')

        self.loadPlugins()
        self.initPlugins()

        self.botinfo = self.bot.get_me()
        self.logger.info('Bot: @%s (%s)', self.botinfo.username, self.botinfo.first_name)

        # Init bot
        self.updater.start_polling()
        self.logger.info('Bot ready')
        self.updater.idle()
        self.logger.info('Bot stopped')

    def loadconfig(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.configFileName)
        self.token = self.config.get('BotConfig', 'token', fallback=defaultExampleToken)
        self.workers = int(self.config.getint('BotConfig', 'workers', fallback=4))
        self.loggerdatefmt = self.config.get('Logging', 'datefmt', fallback="%Y-%m-%d %H:%M:%S")
        self.pluginspath = self.config.get('Plugins', 'path', fallback="plugins")
        self.pluginsextension = self.config.get('Plugins', 'extension', fallback=".plugin.py")

    def setupLogger(self):
        handlers = []
        handlers.append(logging.FileHandler('LLUbot.log'))
        handlers.append(logging.StreamHandler())
        datefmt = self.loggerdatefmt
        logging.basicConfig(format='[%(asctime)s][%(levelname)s] %(message)s', level=logging.INFO, datefmt=datefmt, handlers = handlers)
        self.logger = logging.getLogger(__name__)

    def loadPlugins(self):
        plugins = __import__(self.pluginspath)
        def iter_namespace(ns_pkg):
            return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")
        pluginlist = {
            name: importlib.import_module(name)
            for finder, name, ispkg
            in iter_namespace(plugins)
        }
        self.plugins = {}
        for pluginname, plugin in pluginlist.items():
            self.logger.info('Init plugin: %s' % pluginname)
            self.plugins[pluginname] = plugin.Plugin(main=self, updater=self.updater)

    def initPlugins(self):
        for pluginname, plugin in self.plugins.items():
            if hasattr(plugin, 'postinit'):
                plugin.postinit()

    def getPlugins(self):
        return self.plugins

    def getConfig(self):
        return self.config

if __name__ == '__main__':
    LLUbot('config.ini')

class Plugin:
    def __init__(self, main, updater):
        self.main = main
        self.logger = main.logger

    def postinit(self):
        plugins = self.main.getPlugins()
        pluginnames = [pluginname for pluginname, plugin in plugins.items()]
        self.logger.info("Plugins: %s", pluginnames)

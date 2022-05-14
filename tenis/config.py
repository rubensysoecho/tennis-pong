import json
from importlib import resources

def cfg_item(*items):
    d = Config.instance().data
    for k in items:
        d = d[k]
    return d

class Config:

    __config_json_path, __config_json_filename = "tenis.assets.config", "config.json"
    __instance = None

    @staticmethod
    def instance():
        if Config.__instance is None:
            Config()
        return Config.__instance

    def __init__(self):
        if Config.__instance is None:
            Config.__instance = self

            with resources.path(Config.__config_json_path, Config.__config_json_filename) as config_path:
                with open(config_path) as f:
                    self.data = json.load(f)
            self.__debug = False
        else:
            raise Exception("Config doesn't allow multiple instances")

    @property
    def debug(self):
        return self.__debug

    @debug.setter
    def debug(self,value):
        self.__debug = value

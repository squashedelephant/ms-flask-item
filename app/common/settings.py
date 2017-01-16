
from logging import DEBUG, basicConfig, getLogger
from os.path import exists
from sys import exit
from yaml import load

basicConfig(level=DEBUG,
            filename='/logs/app.log',
            filemode='a',
            format='[%(asctime)s:%(levelname)s %(name)s::%(funcName)s(%(lineno)s)] %(message)s')
log = getLogger(__name__)

class Config:
    @classmethod
    def load_config_file(cls):
        log.info('enter load_config_file')
        config_file = '/config/app.yml'
        if not exists(config_file):
            log.error('Config file: {} not created by consul-template'.format(
                config_file))
            exit(1)
        config = {}
        with open(config_file) as f:
            config = load(f)
        return config

config = Config.load_config_file()


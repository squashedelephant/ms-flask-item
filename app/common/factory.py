
from flask import Flask
from logging import getLogger
from logging.config import dictConfig

from app.common.settings import config
from app.item.apis import apis as item_apis 

log = getLogger(__name__)

def create_app(package_name=__name__, debug=False, threads=True):
    """
    creates the flask app and initializes background threads if any
    """
    app = Flask(package_name)
    app.config.from_object(config['flask'])

    init_logger()
    register_blueprints(app)
    start_threads(threads)
    return app

def init_logger():
    """
    enable logging to /logs/app.log
    """
    dictConfig(config['logging'])
    log.info('app logger initialized')
    return

def register_blueprints(app):
    """
    group similar endpoints as blueprints before registration
    registration enables app to accept HTTP requests for endpoints
    """
    log.info('Registering blueprints')
    blueprints = [item_apis]
    for blueprint in blueprints:
        log.info('Registering {}'.format(blueprint.url_prefix))
        app.register_blueprint(blueprint)
    return

def start_threads(threads):
    """
    primary thread must always listen for HTTP requests, submit CQL to Cassandra
    secondary threads if any are useful for camping on pub/sub or message queues
        but they may die so must be wrapped in monitors
    """
    log.info('enter start_threads')
    return


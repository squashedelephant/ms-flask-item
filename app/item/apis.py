
from flask import Blueprint
from logging import getLogger

from app.common.settings import config
from app.shared.task import Task
from utils.decorator import retry, timeit

host, port = config['service']['ms_item'][0].split(':')
api_version = config['ms_item']['api_version']
api_name = 'item'
api_prefix = '/v{}/{}'.format(config['flask']['api_version'], api_name)
apis = Blueprint(api_name, __name__, url_prefix=api_prefix)

log = getLogger(__name__)
log.info('Listening on {}'.format(api_prefix))

@apis.route('/', methods=['POST'])
@timeit
@retry
def stock(**kwargs):
    """
    stock a new Item object
    assume validation of mandatory args occurs downstream to ease future
    code maintenance
    return value: JSON dict with keys: data, status_code, reason 
                  where data is another dict with keys:
                      item_id, name, description, sku, cost, price,
                      quantity, added, removed, deleted
    """
    url = 'http://{}:{}/v{}/item/'.format(host, port, api_version)
    return Task.forward(url, 'POST')

@apis.route('/list', methods=['PUT'])
@timeit
@retry
def get_all(**kwargs):
    """
    get all Items objects
    assume validation of mandatory args occurs downstream to ease future
    code maintenance
    return value: JSON dict with keys: data, status_code, reason 
                  where data is a list of dict with keys:
                      item_id, name, description, sku, cost, price,
                      quantity, added, removed, deleted
    """
    url = 'http://{}:{}/v{}/item/list'.format(host, port, api_version)
    return Task.forward(url, 'PUT')

@apis.route('/<item_id>', methods=['GET'])
@timeit
@retry
def get_by_id(item_id, **kwargs):
    """
    get existing Item object by item_id
    assume validation of mandatory args occurs downstream to ease future
    code maintenance
    return value: JSON dict with keys: data, status_code, reason 
                  where data is another dict with keys:
                      item_id, name, description, sku, cost, price,
                      quantity, added, removed, deleted
    """
    url = 'http://{}:{}/v{}/item/{}'.format(host,
                                            port,
                                            api_version,
                                            item_id)
    return Task.forward(url, 'GET')

@apis.route('/<item_id>', methods=['PUT'])
@retry
@timeit
def update(item_id, **kwargs):
    """
    modify an existing Item object updating key, value pairs from form data
    assume validation of optional args occurs downstream to ease future
    code maintenance
    return value: JSON dict with keys: data, status_code, reason 
                  where data is another dict with keys:
                      item_id, name, description, sku, cost, price,
                      quantity, added, removed, deleted
    """
    url = 'http://{}:{}/v{}/item/{}'.format(host,
                                            port,
                                            api_version,
                                            item_id)
    return Task.forward(url, 'PUT')

@apis.route('/<item_id>', methods=['DELETE'])
@retry
@timeit
def delete(item_id, **kwargs):
    """
    delete an existing Item object updating key: deleted
    assume validation of mandatory args occurs downstream to ease future
    code maintenance
    return value: JSON dict with keys: data, status_code, reason 
                  where data is an empty list
    """
    url = 'http://{}:{}/v{}/item/{}'.format(host,
                                            port,
                                            api_version,
                                            item_id)
    return Task.forward(url, 'DELETE')

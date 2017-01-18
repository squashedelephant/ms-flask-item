
from flask import Blueprint, jsonify, request
from logging import getLogger
from ujson import loads

from app.common.settings import config
from app.item.task import Task
from app.shared.validate import evaluate_form, evaluate_uuid
from utils.decorator import retry, timeit

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
    validate mandatory args used to stock a new Item object
    mandatory form args:
        name = unicode string
        description = unicode string
        sku = barcode formula
        cost = float in xxxx.yy format
        price = float in xxxx.yy format
        quantity = integer
    return value: JSON dict with keys: data, status_code, reason 
                  where data is another dict with key: item_id
    """
    mandatory_keys = ['name',
                      'description',
                      'sku',
                      'cost',
                      'price',
                      'quantity']
    form = loads(request.data.decode('utf-8'))
    (error, error_msg) = evaluate_form(mandatory_keys, form, mandatory=True)
    if error:
        return jsonify(error_msg)
    return jsonify(Task.stock(form))

@apis.route('/list', methods=['PUT'])
@timeit
@retry
def get_inventory(**kwargs):
    """
    get all Items objects where deleted=False
    mandatory form args:
        offset = starting point within result to return
        limit = chunk size within result to return
    return value: JSON dict with keys: data, status_code, reason 
                  where data is a list of dict with keys:
                      item_id, name, description, sku, cost, price,
                      quantity, added, removed, deleted
    """
    mandatory_keys = ['offset',
                      'limit']
    form = loads(request.data.decode('utf-8'))
    (error, error_msg) = evaluate_form(mandatory_keys, form, mandatory=True)
    if error:
        return jsonify(error_msg)
    return jsonify(Task.get_inventory(form))

@apis.route('/<item_id>', methods=['GET'])
@timeit
@retry
def get_by_id(item_id, **kwargs):
    """
    get existing Item object by item_id
    mandatory args:
        item_id = valid UUID
    return value: JSON dict with keys: data, status_code, reason 
                  where data is another dict with keys:
                      item_id, name, description, sku, cost, price,
                      quantity, added, removed, deleted
    """
    (error, error_msg) = evaluate_uuid(item_id)
    if error:
        return jsonify(error_msg)
    return jsonify(Task.get_by_id(item_id))

@apis.route('/<item_id>', methods=['PUT'])
@retry
@timeit
def update(item_id, **kwargs):
    """
    modify an existing Item object updating key, value pairs from form data
    mandatory args:
        item_id = valid UUID
    optional form args:
        name = unicode string
        description = unicode string
        sku = barcode formula
        cost = float in xxxx.yy format
        price = float in xxxx.yy format
        quantity = integer
    return value: JSON dict with keys: data, status_code, reason 
                  where data is another dict with keys:
                      item_id, name, description, sku, cost, price,
                      quantity, added, removed, deleted
    return value: JSON dict with keys: data, status_code, reason 
                  where data is an empty list
    """
    optional_keys = ['name',
                      'description',
                      'sku',
                      'cost',
                      'price',
                      'quantity']
    form = loads(request.data.decode('utf-8'))
    form['item_id'] = item_id
    (error, error_msg) = evaluate_form(optional_keys, form)
    if error:
        return jsonify(error_msg)
    (error, error_msg) = evaluate_uuid(item_id)
    if error:
        return jsonify(error_msg)
    return jsonify(Task.update(form))

@apis.route('/<item_id>', methods=['DELETE'])
@retry
@timeit
def delete(item_id, **kwargs):
    """
    delete an existing Item object updating key: deleted
    mandatory args:
        item_id = valid UUID
    return value: JSON dict with keys: data, status_code, reason 
                  where data is an empty list
    """
    (error, error_msg) = evaluate_uuid(item_id)
    if error:
        return jsonify(error_msg)
    return jsonify(Task.delete(item_id))

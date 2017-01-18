
from flask import jsonify, request
from logging import getLogger
from requests import ConnectionError, Session
from ujson import loads
from uuid import uuid4

from app.common.settings import config
from app.shared.cql import CQL
from app.shared.dsl import DSL
from app.shared.item import Item
from app.item.storage import Storage
from utils.timestamp import MSdate

log = getLogger(__name__)

class Task:
    @classmethod
    def stock(cls, form):
        """
        create a new Item object by submitting SQL INSERT and
        mapped values to Cassandra then same values to ElasticSearch
        mandatory args:
            form = dict of CQL table columns as keys and values as values
        """
        item_id = uuid4()
        form['item_id'] = item_id
        form['added'] = MSdate.get_current_time()
        form['removed'] = -1
        form['deleted'] = False
        (sql, values) = CQL.build_insert_create(form)
        result = Storage.cql_es_write(sql, values, 'create')
        if result['status_code'] in [2006, 3006]:
            result['data'] = {'item_id': item_id}
        return result

    @classmethod
    def get_inventory(cls, form):
        """
        retrieve existing Item objects by submitting DSL query to ElasticSearch
        mandatory args:
            form = dict of keys: offset, limit
        """
        (dsl, fields) = DSL.build_query_active(form['offset'], form['limit'])
        return Storage.es_search(dsl=dsl, fields=fields)

    @classmethod
    def get_by_id(cls, item_id):
        """
        retrieve existing Item object where item_id=<item_id> AND deleted=False
        mandatory args:
            item_id = valid UUID
        """
        (dsl, fields) = DSL.build_query_item_id(item_id)
        values = {}
        values['item_id'] = item_id
        values['doc_id'] = item_id
        return Storage.es_read(values=values, dsl=dsl, fields=fields)

    @classmethod
    def update(cls, form):
        """
        modify an existing Item object by submitting SQL UPDATE and mapped
        values to Cassandra and updated fields to ElasticSearch index
        mandatory args:
            form = dict of CQL table columns as keys and values as values
        """
        (sql, values) = CQL.build_insert_update(form)
        result = Storage.cql_es_write(sql, values, 'update')
        if result['status_code'] in [2006, 3007]:
            result['data'] = {'item_id': form['item_id']}
        return result

    @classmethod
    def delete(cls, item_id):
        """
        delete an existing Item object by setting attribute deleted=True
        mandatory args:
            item_id = valid UUID
        """
        (sql, values) = CQL.build_update_delete(item_id)
        result = Storage.cql_es_write(sql, values, 'update')
        if result['status_code'] in [2006, 3006]:
            result['data'] = {'item_id': item_id}
        return result

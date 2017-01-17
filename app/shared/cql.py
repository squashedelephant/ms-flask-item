
from logging import getLogger
from uuid import UUID

from app.common.settings import config

log = getLogger(__name__)

class CQL:
    keyspace = config['cql']['keyspace']
    table = config['cql']['table']
    columns = ['item_id', 'name', 'description', 'sku', 'cost', 'price',
               'quantity', 'added', 'removed', 'deleted']
    immutable_columns = ['item_id']

    @classmethod
    def build_insert_create(cls, d):
        """
        build CQL INSERT statement using placeholders for values passed in as 
        a dict and bound dynamically values dict is unchanged incoming dict
        because data types already pre-defined by calling function
        """
        sql = 'INSERT INTO {}.{}('.format(cls.keyspace, cls.table)
        values = ''
        for key, val in d.items():
            sql += '{}, '.format(key)
            values += '%({})s, '.format(key)
        sql = '{}) VALUES({});'.format(sql[0:-2], values[0:-2])
        log.debug('SQL: {}'.format(sql))
        return (sql, d)

    @classmethod
    def build_insert_update(cls, values):
        """
        build CQL UPDATE statement for single row identified by PK = item_id
        sql: CQL statement
        values: critical columns
        """
        item_id = values['item_id']
        sql = "UPDATE {}.{} SET ".format(cls.keyspace,
                                         cls.table)
        for k, v in values.items():
            if k in cls.immutable_columns:
                continue
            sql += "{}=%({})s, ".format(k, k)
        sql = sql[0:-2]
        sql += " WHERE item_id=%(item_id)s;"
        if isinstance(values['item_id'], str):
            values['item_id'] = UUID(item_id)
        log.debug('SQL: {}'.format(sql))
        log.debug('values: {}'.format(values))
        return (sql, values)

    @classmethod
    def build_query_active(cls):
        """
        build CQL SELECT statement of all rows 
        sql: CQL statement
        values: critical columns
        Note: this feature requires reading from ElasticSearch
        """
        sql = 'SELECT '
        for key in cls.columns:
            sql += '{}, '.format(key)
        sql = sql[0:-2]
        sql += " FROM {}.{};".format(cls.keyspace, cls.table)
        log.debug('SQL: {}'.format(sql))
        return (sql, cls.columns)
     
    @classmethod
    def build_query_item_id(cls, item_id):
        """
        build CQL SELECT statement for single row identified by PK = item_id
        """
        sql = 'SELECT '
        for key in cls.columns:
            sql += '{}, '.format(key)
        sql = sql[0:-2]
        sql += " FROM {}.{} WHERE item_id={} AND status='ACTIVE' AND deleted=False;".format(
            cls.keyspace,
            cls.table,
            item_id)
        values = {}
        values['item_id'] = UUID(item_id)
        log.debug('SQL: {}'.format(sql))
        log.debug('values: {}'.format(values))
        return (sql, values)

    @classmethod
    def build_update_delete(cls, item_id):
        """
        build CQL UPDATE statement for single row SET deleted=True 
        identified by PK
        """
        sql = 'UPDATE {}.{} '.format(cls.keyspace,
                                     cls.table)
        sql += 'SET deleted=%(deleted)s WHERE item_id=%(item_id)s;'
        values = {}
        values['deleted'] = True
        if isinstance(item_id, str):
            values['item_id'] = UUID(item_id)
        else:
            values['item_id'] = item_id
        log.debug('SQL: {}'.format(sql))
        log.debug('values: {}'.format(values))                                                                                   
        return (sql, values)                                                                                                     


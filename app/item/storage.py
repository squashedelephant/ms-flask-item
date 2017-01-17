
from logging import getLogger

from app.common.settings import config
from app.shared.formatters import Format

from connectors.cassandra.my_cassandra import CQLConnector
from connectors.elasticsearch.my_elasticsearch import ESConnector

log = getLogger(__name__)

class Storage:
    cql_local_env = config['cql']['local_env']
    cql_hosts = config['cql']['hosts']
    cql_port = int(config['cql']['port'])
    cql_keyspace = config['cql']['keyspace']
    cql_timeout = config['cql']['timeout']
    es_local_env = config['es']['local_env']
    es_host = config['es']['host']
    es_port = int(config['es']['port'])
    es_index = config['es']['index_name']
    es_doc_type = config['es']['doc_type']
    es_settings = config['es']['settings']
    es_mappings = config['es']['index_mappings']
    es_timeout = config['es']['timeout']
    es_limit = config['es']['limit']
    es_offset = config['es']['offset']

    @classmethod
    def cql_write(cls, sql, values, action):
        c = CQLConnector(hosts=cls.cql_hosts,
                         keyspace=cls.cql_keyspace,
                         local_env=cls.cql_local_env,
                         connect_timeout=cls.cql_timeout)
        return c.write(sql, values)

    @classmethod
    def cql_es_write(cls, sql, values, action):
        c = CQLConnector(hosts=cls.cql_hosts,
                         keyspace=cls.cql_keyspace,
                         local_env=cls.cql_local_env,
                         connect_timeout=cls.cql_timeout)
        cql_result = c.write(sql, values)
        if cql_result['status_code'] != 2006:
            return cql_result
        log.info('Successfully stored in Cassandra')
        if action == 'create':
            es_data = Format.cql_to_es_create(values)
            log.info('es_data: {}'.format(es_data))
            return cls.es_create(cql_result, es_data)
        elif action == 'update':
            es_data = Format.cql_to_es_update(values)
            log.info('es_data: {}'.format(es_data))
            return cls.es_update(cql_result, es_data)

    @classmethod
    def cql_read(cls, sql, values):
        c = CQLConnector(hosts=cls.cql_hosts,
                         keyspace=cls.cql_keyspace,
                         local_env=cls.cql_local_env,
                         connect_timeout=cls.cql_timeout)
        return c.read(sql, values)

    @classmethod
    def es_create(cls, cql_result, es_data):
        es = ESConnector(host=cls.es_host,
                         port=cls.es_port,
                         timeout=cls.es_timeout,
                         local_env=cls.es_local_env)
        es_result = es.add_document(index=cls.es_index,
                                    doc_type=cls.es_doc_type,
                                    doc_id=es_data['doc_id'],
                                    settings=cls.es_settings,
                                    mappings=cls.es_mappings,
                                    values=es_data)
        if 'created' in es_result and es_result['created']:
            log.info('Successfully stored in ElasticSearch')
            return cql_result
        return es_result

    @classmethod
    def es_update(cls, cql_result, es_data):
        es = ESConnector(host=cls.es_host,
                         port=cls.es_port,
                         timeout=cls.es_timeout,
                         local_env=cls.es_local_env)
        es_result = es.update_document(index=cls.es_index,
                                       doc_type=cls.es_doc_type,
                                       doc_id=es_data['doc']['doc_id'],
                                       values=es_data)
        if '_version' in es_result['data'] and es_result['data']['_version'] > 0:
            log.info('Successfully updated ElasticSearch')
        return es_result

    @classmethod
    def es_read(cls, values=None, dsl=None, fields=None):
        es = ESConnector(host=cls.es_host,
                         local_env=cls.es_local_env,
                         timeout=cls.es_timeout)
        es_result = es.find_document(index=cls.es_index,
                                     doc_type=cls.es_doc_type,
                                     dsl=dsl,
                                     fields=fields)
        if dsl['from'] + dsl['size'] < es_result['data']['hits']['total']:
            es_result['data']['next_offset'] = dsl['from'] + dsl['size']
        else:
            es_result['data']['next_offset'] = -1
        log.info('ES result: {}'.format(es_result))
        return es_result

    @classmethod
    def es_search(cls, dsl=None, fields=None):
        es = ESConnector(host=cls.es_host,
                         local_env=cls.es_local_env,
                         timeout=cls.es_timeout)
        es_result = es.search_documents(index=cls.es_index,
                                        doc_type=cls.es_doc_type,
                                        dsl=dsl,
                                        fields=fields)
        if dsl['from'] + dsl['size'] < es_result['data']['hits']['total']:
            es_result['data']['next_offset'] = dsl['from'] + dsl['size']
        else:
            es_result['data']['next_offset'] = -1
        log.info('ES result: {}'.format(es_result))
        return es_result

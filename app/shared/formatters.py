
from logging import getLogger
from uuid import UUID

log = getLogger(__name__)

class Format:
    @classmethod
    def cql_to_es_create(cls, d):
        new_dict = d.copy()
        for k, v in d.items():
            if isinstance(v, tuple):
                new_list = []
                for e in v:
                    if isinstance(e, UUID):
                        new_list.append(str(e))
                    else:
                        new_list.append(e)
                new_dict[k] = new_list
            elif isinstance(v, UUID):
                new_dict[k] = str(v)
            elif isinstance(v, bool):
                new_dict[k] = str(v).lower()
            elif isinstance(v, bytes):
                new_dict[k] = str(v)
            if k.endswith('_id'):
                new_dict['doc_id'] = str(v)
        return new_dict

    @classmethod
    def cql_to_es_update(cls, d):
        new_dict = {'doc': {}}
        for k, v in d.items():
            if isinstance(v, tuple):
                new_list = []
                for e in v:
                    if isinstance(e, UUID):
                        new_list.append(str(e))
                    else:
                        new_list.append(e)
                new_dict['doc'][k] = new_list
            elif isinstance(v, UUID):
                new_dict['doc'][k] = str(v)
            elif isinstance(v, bool):
                new_dict['doc'][k] = str(v).lower()
            elif isinstance(v, bytes):
                new_dict['doc'][k] = str(v)
            if k.endswith('_id'):
                new_dict['doc']['doc_id'] = str(v)
        return new_dict


from logging import getLogger
from uuid import UUID

from app.common.settings import config

log = getLogger(__name__)

class DSL:
    index = config['es']['index_name']
    doc_type = config['es']['doc_type']
    columns = ['item_id', 'name', 'description', 'sku', 'cost', 'price',
               'quantity', 'added', 'removed', 'deleted']

    @classmethod
    def build_query_active(cls, offset=0, limit=1):
        return ({"from": offset,
                "size": limit,
                "query": {"match": {"deleted": False}}}
                cls.columns)

    @classmethod
    def build_query_item_id(cls, item_id, offset=0, limit=1):
        return ({"from": offset,
                "size": limit,
                "query": {"match": {"item_id": item_id},
                          "match": {"deleted": False}}}
                cls.columns)

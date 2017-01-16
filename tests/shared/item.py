
from ujson import load

class Item:
    @staticmethod
    def _load_fixture(f):
        try:
            fh = open(f, 'r')
            d = load(fh)
            fh.close()
            return d
        except IOError as e:
            #print(e)
            exit('ERROR: unable to read fixture: {}'.format(f))

    @staticmethod
    def get_new_item():
        fixture = '../../fixtures/item/new_item.json'
        return Item._load_fixture(fixture)

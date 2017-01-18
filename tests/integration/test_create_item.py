#!/usr/bin/env python3

from requests import ConnectionError, Session
from ujson import dumps
from unittest import TestCase, main
from uuid import UUID

from utils.test.dependent import Dependent
from utils.test.header import Header
from tests.shared.item import Item

class TestCreateItem(TestCase):
    def setUp(self):
        self.host = Dependent.get_vm_host()
        self.port = Dependent.services['ms_item']
        self.headers = Header.get_headers()
        self.url = 'http://{}:{}/v1.0/item/'.format(self.host, self.port)
        self.s = None
        self.r = None
        Dependent.validate_required_services(['cassandra', 'elasticsearch'])

    def tearDown(self):
        pass

    def _manage_request(self, payload):
        try:
            self.s = Session()
            self.r = self.s.post(self.url, data=dumps(payload), headers=self.headers)
            return
        except ConnectionError as e:
            exit('ERROR: unknown exception: {}'.format(str(e)))

    def test_01_create_new_item(self):
        """
        validate ability to create an Item object
        """
        self._manage_request(Item.get_new_item())
        self.assertEqual(200, self.r.status_code)
        self.assertEqual('OK', self.r.reason)
        response = self.r.json()
        self.assertEqual("object created successfully", response['reason'])
        self.assertEqual(3006, response['status_code'])
        self.assertIn('item_id', response['data'])
        self.assertIsInstance(UUID(response['data']['item_id']), UUID)
        # response time < 100ms
        self.assertGreater(100, response['access_time'])

if __name__ == '__main__':
    main()


from gevent.wsgi import WSGIServer
from unittest import TestCase, main

from app.common.main import app

class TestMain(TestCase):
    def setUp(self):
        self.server = None 

    def tearDown(self):
        pass

    def test_01_get_flask_app(self):
        self.assertEquals('ms_item', app.name)

    def test_02_run_app_as_server(self):
        self.server = WSGIServer(('', 81), app)
        self.assertEquals(('', 81), self.server.address)

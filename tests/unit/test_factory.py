
from flask import Flask
from gevent.wsgi import WSGIServer
from unittest import TestCase, main

from app.common.factory import init_logger, register_blueprints, start_threads

class TestFactory(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_01_logger(self):
        try:
            init_logger()
            self.assertTrue(True)
        except Exception as e:
            print(str(e))
            self.assertTrue(False)

    def test_02_blueprints(self):
        app = Flask(__name__)
        register_blueprints(app)
        expected_blueprints = ['item']
        for bp in expected_blueprints:
            self.assertIn(bp, app.blueprints.keys())

    def test_03_threads(self):
        try:
            start_threads(threads=True)
            self.assertTrue(True)
        except Exception as e:
            print(str(e))
            self.assertTrue(False)


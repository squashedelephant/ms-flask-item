
from unittest import TestCase, main

from app.common.settings import config

class TestMain(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_01_load_config(self):
        expected_keys = ['flask', 'aws', 'sqs', 'sns', 'service', 'cql', 'es', 'log_level', 'logging']
        self.assertEqual(len(expected_keys), len(config.keys()))

    def test_02_flask_subkeys(self):
        expected_keys = ['api_version', 'debug']
        self.assertEqual(len(expected_keys), len(config['flask']))
        for ek in expected_keys:
            self.assertIn(ek, config['flask'])

    def test_03_aws_subkeys(self):
        expected_keys = ['access_key', 'secret_access_key', 'region']
        self.assertEqual(len(expected_keys), len(config['aws']))
        for ek in expected_keys:
            self.assertIn(ek, config['aws'])

    def test_04_sqs_subkeys(self):
        expected_keys = ['retry_limit', 'queue_name']
        self.assertEqual(len(expected_keys), len(config['sqs']))
        for ek in expected_keys:
            self.assertIn(ek, config['sqs'])

    def test_05_sns_subkeys(self):
        expected_keys = ['retry_limit', 'topic_name']
        self.assertEqual(len(expected_keys), len(config['sns']))
        for ek in expected_keys:
            self.assertIn(ek, config['sns'])

    def test_06_service_subkeys(self):
        expected_keys = ['max_attempts']
        self.assertEqual(len(expected_keys), len(config['service']))
        for ek in expected_keys:
            self.assertIn(ek, config['service'])

    def test_07_cql_subkeys(self):
        expected_keys = ['local_env', 'hosts', 'port', 'keyspace', 'table', 'timeout']
        self.assertEqual(len(expected_keys), len(config['cql']))
        for ek in expected_keys:
            self.assertIn(ek, config['cql'])

    def test_08_es_subkeys(self):
        expected_keys = ['local_env', 'host', 'port', 'index_name', 'doc_type',
                         'timeout', 'limit', 'offset', 'settings', 'index_mappings']
        self.assertEqual(len(expected_keys), len(config['es']))
        for ek in expected_keys:
            self.assertIn(ek, config['es'])

    def test_09_logging_subkeys(self):
        expected_keys = ['version', 'disable_existing_loggers', 'formatters',
                         'handlers', 'loggers']
        self.assertEqual(len(expected_keys), len(config['logging']))
        for ek in expected_keys:
            self.assertIn(ek, config['logging'])


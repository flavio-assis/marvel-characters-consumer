from unittest import TestCase

from src.models.connection import Connection


class TestModelConnection(TestCase):
    def setUp(self) -> None:
        self.public_api_key = 'public'
        self.private_api_key = 'private'
        self.conn = Connection(self.public_api_key, self.private_api_key)

    def test_connection_correct_load_params(self):
        expected_output = [self.public_api_key, self.private_api_key]
        self.assertEqual([self.conn.public_api_key, self.conn.private_api_key], expected_output)

    def test_connection_has_attribute_public_key(self):
        assert hasattr(self.conn, 'public_api_key')

    def test_connection_has_attribute_private_key(self):
        assert hasattr(self.conn, 'private_api_key')

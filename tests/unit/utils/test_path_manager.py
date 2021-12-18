import os
from unittest import TestCase
from unittest.mock import patch

from src.utils.path_manager import construct_path


class TestPathManager(TestCase):
    def setUp(self) -> None:
        self.path = "layer"
        self.src_dir = '/'.join(os.path.dirname(__file__).split('/')[:-3])

    @patch('os.makedirs')
    def test_construct_path(self, mock_makedirs):
        expected_output = os.path.join(self.src_dir, 'src', 'utils', '..', '..', 'layer')
        actual_output = construct_path(self.path)
        self.assertEqual(expected_output, actual_output)

import os
from unittest import TestCase

import pandas as pd

from src.data_processing.cleaning import CharacterDataFrameCleaning


class TestCleanDataframe(TestCase):
    def setUp(self) -> None:
        self.raw_path = os.path.join(os.path.dirname(__file__), 'files/raw')
        self.cleaned_path = os.path.join(os.path.dirname(__file__), 'files/cleaned')

    def test_write_dataframe_and_get_results(self):
        processor = CharacterDataFrameCleaning(self.raw_path)
        processor.clean_results(
            columns_to_drop=['id'],
            get_nested_value={
                'columns': ['category'],
                'property': 'color'
            }
        )
        data = {
            'category': ['red', 'white', 'black', 'violet']
        }

        expected_output = pd.DataFrame(data)

        actual_output = processor.df

        self.assertTrue(expected_output.equals(actual_output))
        processor.sink_data_frame(self.cleaned_path)

        expected_file_output = ['characters-cleaned.json']
        self.assertEqual(expected_file_output, os.listdir(self.cleaned_path))
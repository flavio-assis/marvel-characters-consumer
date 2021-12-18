from unittest import TestCase
from unittest.mock import patch

import pandas as pd
from src.data_processing.cleaning import CharacterDataFrameCleaning


class TestDataProcessingCleaning(TestCase):

    @patch('src.data_processing.cleaning.CharacterDataFrameCleaning.load_data_frame')
    def setUp(self, mocked_load_dataframe) -> None:
        self.data = {
            'col1': [{"available": 1, "types": "b"}, {"available": 3, "types": "a"}],
            'col2': [3, 4],
            'col3': ['apple', 'grape']
        }
        mocked_load_dataframe.return_value = pd.DataFrame(self.data)
        self.character_processing = CharacterDataFrameCleaning(source_path='foo')

    @patch('pandas.DataFrame.to_json')
    def test_sink_data_frame(self, mock_df_to_json):
        self.character_processing.sink_data_frame(output_path='foo')

        mock_df_to_json.assert_called_once_with('foo/characters-cleaned.json', orient='records', lines=True)

    def test_get_column_value(self):
        data_before_get_value = {
            'col1': [{"available": 1, "types": "b"}, {"available": 3, "types": "a"}]
        }
        df = pd.DataFrame(data_before_get_value)

        data_after_get_value = {
            'col1': [1, 3]
        }

        expected_output = pd.DataFrame(data_after_get_value)
        actual_output = self.character_processing.get_column_value(df, property_name='available')

        self.assertTrue(expected_output.equals(actual_output))

    def test_clean_results(self):
        columns_to_drop = ['col3']
        get_nested_value = {
            'columns': ['col1'],
            'property': 'available'
        }

        data = {
            'col1': [1, 3],
            'col2': [3, 4]
        }

        expected_output = pd.DataFrame(data)

        self.character_processing.clean_results(columns_to_drop, get_nested_value)
        actual_output = self.character_processing.df

        self.assertTrue(expected_output.equals(actual_output))


class TestDataProcessingCleaningLoadDataFrame(TestCase):

    @patch('src.data_processing.cleaning.CharacterDataFrameCleaning._get_filepaths')
    def test_load_data_frame(self, mock_filepaths):
        filepaths = [
            '[{"col1": "a", "col2": "1"}]',
            '[{"col1": "b", "col2": "2"}]',
            '[{"col1": "c", "col2": "3"}]',
        ]
        mock_filepaths.return_value = filepaths

        data_expected_output = {
            'col1': ['a', 'b', 'c'],
            'col2': [1, 2, 3]
        }
        expected_output = pd.DataFrame(data_expected_output)
        actual_output = CharacterDataFrameCleaning(source_path='foo').df

        self.assertTrue(expected_output.equals(actual_output))

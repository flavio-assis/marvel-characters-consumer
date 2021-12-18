import os

import pandas as pd
from pandas import DataFrame


class CharacterDataFrameCleaning:
    def __init__(self, source_path: str):
        """
        Transform the input json folder in DataFrame
        :param source_path: Path where are located the json files
        """
        self.source_path = source_path
        self.df = self.load_data_frame()

    def _get_filepaths(self):
        return [
            os.path.join(
                self.source_path, file_name
            ) for file_name in os.listdir(self.source_path) if file_name.endswith('.json')
        ]

    def load_data_frame(self) -> DataFrame:
        """
        Loads the DataFrame to the given the self.source_path
        :return: Character Raw DataFrame
        """
        filepaths = self._get_filepaths()

        df = pd.concat(map(pd.read_json, filepaths)).reset_index(drop=True)
        return df

    def sink_data_frame(self, output_path: str) -> None:
        """
        Write the DataFrame to the given output_path
        :param output_path: Path which the DataFrame will be written in format json
        """
        self.df.to_json(os.path.join(output_path, 'characters-cleaned.json'), orient='records', lines=True)

    @staticmethod
    def get_column_value(df: DataFrame, property_name: str) -> DataFrame:
        """

        :param df: Input DataFrame
        :param property_name: Name of the property that will be unnested
        :return: DataFrame with unnested fields
        """
        return df.applymap(lambda x: dict(x).get(property_name))

    def clean_results(self, columns_to_drop: list[str], get_nested_value: dict[str]):
        """
        Performs the cleaning process over the DataFrame
        :param columns_to_drop: List of columns to drop
        :param get_nested_value: Python dict with the name of the columns and the property to be unnested.
          Example:
            get_nested_value={
              'columns': ['comics', 'series', 'stories', 'events'],
              'property': 'available'
            }
        """
        _df = self.df.drop(columns=columns_to_drop)
        _df[get_nested_value.get('columns')] = self.get_column_value(
            self.df[get_nested_value.get('columns')], get_nested_value.get('property')
        )

        self.df = _df

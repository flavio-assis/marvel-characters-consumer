import asyncio
import json
import os
from datetime import datetime
from hashlib import md5
from math import ceil

from aiohttp import ClientSession

from src.models.connection import Connection
from src.utils.logger import logger


class MarvelCharacterHook:
    def __init__(self, url: str, session: ClientSession, connection: Connection):
        """
        Marvel Character Hook to interact with the API
        :param url: URL to request for
        :param session: HTTP Session
        :param connection: Class Connection provided for abstracting keys from connection
        """
        self.url = url
        self.session = session
        self.public_api_key = connection.public_api_key
        self.private_api_key = connection.private_api_key
        self.total_record_count = None

    def _construct_hash(self, ts: str) -> str:
        """
        Hash constructor
        :param ts:
        :return: MD5 hash to use with as query parameter
        """
        return md5(f'{ts}{self.private_api_key}{self.public_api_key}'.encode()).hexdigest()

    async def get_characters_from_api(self, batch: int, offset: int = 0) -> dict:
        """
        Gets data asynchronously from Marvel's Character API.
        :param batch: Batch size to fetch on request
        :param offset: Offset value for fetching the API
        :return: Python dict with response json
        """
        try:
            ts = int(datetime.now().timestamp())

            response = await self.session.request(
                method='GET',
                url=self.url,
                params={
                    'limit': batch,
                    'ts': ts,
                    'offset': offset,
                    'apikey': self.public_api_key,
                    'hash': self._construct_hash(ts=ts)
                }
            )

            logger.debug(f'Response status ({self.url}): {response.status}')
            response_json = await response.json()
            return response_json['data']

        except Exception as err:
            logger.error(f'An error occurred while fetching characters: {err}')
            raise err

    async def get_character_count(self) -> int:
        """
        Get characters count asynchronously
        :return: Total number of characters
        """
        try:
            result = await self.get_characters_from_api(batch=1)
            total = result['total']
            logger.info(f'{total} Results found')
            return total

        except Exception as err:
            logger.error(f'An error occurred while fetching characters count: {err}')
            raise err

    async def get_raw_results(self, output_path: str, batch: int, offset: int) -> None:
        """
        Get API results asynchronously and save them as json files
        :param output_path: Output path for the results json
        :param batch: Batch size to fetch on request
        :param offset: Offset value for fetching the API
        """
        try:
            response = await self.get_characters_from_api(batch, offset)
            results = response['results']
            file_name = f'characters-{offset}-{min(self.total_record_count, offset + batch)}.json'

            logger.debug(f'Writing file: {file_name}')
            with open(os.path.join(output_path, file_name), 'w+') as file:
                file.write(json.dumps(results))

        except Exception as err:
            logger.error(f'An error occurred while fetching characters info: {err}')
            raise err

    async def download_characters(self, output_path: str, batch: int) -> None:
        """
        Wrapper function for self.get_raw_results
        :param output_path: Output path for the results json
        :param batch: Batch size to fetch on request
        """
        self.total_record_count = await self.get_character_count()
        await asyncio.gather(
            *[self.get_raw_results(output_path, batch, batch*i) for i in range(ceil(self.total_record_count/batch))]
        )

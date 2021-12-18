import os
from unittest.mock import patch, AsyncMock

from aiounittest import AsyncTestCase

from src.api.hook import MarvelCharacterHook
from src.models.connection import Connection
from tests.utils.response_mocker import MockResponse


class TestGetRawResults(AsyncTestCase):
    @patch('aiohttp.ClientSession', new_callable=AsyncMock)
    def setUp(self, mock_session) -> None:
        mock_session.request.return_value = MockResponse(json_data={
            'data': {
                'total': 4,
                'results': [
                    {'id': 1, 'category': {'color': 'red', 'type': 'a'}},
                    {'id': 2, 'category': {'color': 'white', 'type': 'b'}},
                    {'id': 3, 'category': {'color': 'black', 'type': 'c'}},
                    {'id': 4, 'category': {'color': 'violet', 'type': 'd'}}
                ]
            }
        },
            status_code=200
        )

        self.conn = Connection('abc', 'zyx')
        self.hook = MarvelCharacterHook(
            url='foo.com',
            session=mock_session,
            connection=self.conn
        )
        self.raw_path = os.path.join(os.path.dirname(__file__), 'files/raw')

    async def test_download_characters(self):
        await self.hook.download_characters(output_path=self.raw_path, batch=4)

        expected_output = ['characters-0-4.json']
        self.assertEqual(expected_output, os.listdir(self.raw_path))

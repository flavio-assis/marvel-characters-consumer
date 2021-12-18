from unittest.mock import patch, AsyncMock

from aiounittest import AsyncTestCase

from src.api.hook import MarvelCharacterHook
from src.models.connection import Connection
from tests.utils.response_mocker import MockResponse


class TestMarvelCharacterHookApi(AsyncTestCase):

    @patch('aiohttp.ClientSession', new_callable=AsyncMock)
    def setUp(self, mock_session) -> None:
        mock_session.request.return_value = MockResponse(json_data={
            'data': {
                'total': 20,
                'results': [
                    {'id': 1},
                    {'id': 2}
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

    def test_construct_hash(self):
        expected_output = '3b5c7d57febb38d26bc7116853b5d207'

        self.assertEqual(expected_output, self.hook._construct_hash(ts='1639788219'))

    async def test_get_characters_from_api(self):
        response = await self.hook.get_characters_from_api(batch=1)

        expected_output = {
            'total': 20,
            'results': [
                {'id': 1},
                {'id': 2}
            ]
        }

        self.assertEqual(expected_output, response)

    @patch('src.api.hook.MarvelCharacterHook.get_characters_from_api')
    async def test_get_character_count(self, mock_session_request):
        mock_session_request.return_value = {'total': 20}

        self.assertEqual(await self.hook.get_character_count(), 20)

    @patch('src.api.hook.MarvelCharacterHook.get_characters_from_api')
    @patch('builtins.open')
    async def test_get_raw_results(self, mock_open, mock_session_request):
        mock_session_request.return_value = {'results': [{'id': 1}, {'id': 2}]}
        self.hook.total_record_count = 20

        await self.hook.get_raw_results(output_path='foo', batch=10, offset=0)

        mock_open.assert_called_once_with('foo/characters-0-10.json', 'w+')

    @patch('src.api.hook.MarvelCharacterHook.get_character_count')
    @patch('src.api.hook.MarvelCharacterHook.get_raw_results')
    async def test_download_characters(self, mock_get_raw_results, mock_get_characters_count):
        await self.hook.download_characters(output_path='foo', batch=100)

        mock_get_characters_count.assert_called_once()
        mock_get_raw_results.assert_called_once()

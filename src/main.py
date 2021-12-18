import asyncio
import os
from argparse import ArgumentParser
from datetime import datetime

from aiohttp import ClientSession

from src.api.hook import MarvelCharacterHook
from src.data_processing.cleaning import CharacterDataFrameCleaning
from src.models.connection import Connection
from src.utils.logger import logger
from src.utils.path_manager import construct_path

URL: str = 'http://gateway.marvel.com/v1/public/characters'

MARVEL_PUBLIC_API_KEY = os.environ.get('MARVEL_PUBLIC_API_KEY')
MARVEL_PRIVATE_API_KEY = os.environ.get('MARVEL_PRIVATE_API_KEY')
APP_HOME = os.environ.get('APP_HOME', os.environ.get('PWD'))

parser = ArgumentParser(description='Command line input for Marvel Character API Consumer')
parser.add_argument(
    '--batch',
    dest='batch',
    type=int,
    required=False,
    default=100,
    help='Limit of results for each API get request'
)
parser.add_argument(
    '--raw-path',
    dest='raw_path',
    type=str,
    required=False,
    default=os.path.join(APP_HOME, 'results/raw'),
    help='Output path for download json files'
)
parser.add_argument(
    '--cleaned-path',
    dest='cleaned_path',
    type=str,
    required=False,
    default=os.path.join(APP_HOME, 'results/cleaned'),
    help='Output path for the cleaned DataFrame'
)

args, _ = parser.parse_known_args()


async def runner():
    execution_datetime = datetime.now().isoformat()
    output_raw_path = os.path.join(args.raw_path, execution_datetime)
    output_cleaned_path = os.path.join(args.cleaned_path, execution_datetime)

    async with ClientSession() as session:
        logger.info('Getting character from Marvel API')

        marvel_connection = Connection(
            public_api_key=MARVEL_PUBLIC_API_KEY,
            private_api_key=MARVEL_PRIVATE_API_KEY
        )

        hook = MarvelCharacterHook(
            url=URL,
            session=session,
            connection=marvel_connection
        )

        await hook.download_characters(
            construct_path(output_raw_path),
            args.batch
        )

    processor = CharacterDataFrameCleaning(source_path=construct_path(output_raw_path))
    processor.clean_results(
        columns_to_drop=['modified', 'thumbnail', 'resourceURI', 'urls'],
        get_nested_value={
            'columns': ['comics', 'series', 'stories', 'events'],
            'property': 'available'
        }
    )
    processor.sink_data_frame(output_path=construct_path(output_cleaned_path))
    logger.info(processor.df)


def main():
    asyncio.run(runner())


if __name__ == '__main__':
    main()

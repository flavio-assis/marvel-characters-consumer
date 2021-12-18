import logging
from io import StringIO
from unittest import TestCase

from src.utils.logger import logger


def foo():
    logger.info('It works!')


class TestLoggerUtils(TestCase):
    def setUp(self) -> None:
        self.stream = StringIO()
        self.handler = logging.StreamHandler(self.stream)
        for handler in logger.handlers:
            logger.removeHandler(handler)
        logger.addHandler(hdlr=self.handler)

    def test_logger_output(self):
        expected_output = 'It works!'
        foo()
        actual_output = self.stream.getvalue().strip()
        self.assertEqual(expected_output, actual_output)

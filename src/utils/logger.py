import os
from logging import getLogger, StreamHandler

logger = getLogger(__name__)
logger.setLevel(os.getenv('LOG_LEVEL', 'INFO'))
logger.addHandler(StreamHandler())

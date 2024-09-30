import logging
import sys

from logging.handlers import RotatingFileHandler

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

logging.getLogger('discord.http').setLevel(logging.INFO)

stream_handler = logging.StreamHandler(stream=sys.stdout)
file_handler = RotatingFileHandler(
    filename='slugsnet.log',
    backupCount=5
)

logging.basicConfig(
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[stream_handler, file_handler]
)

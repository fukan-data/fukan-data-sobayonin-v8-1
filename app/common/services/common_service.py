import environ
import os
import pytz
import re
from time import sleep
from datetime import datetime, timedelta, timezone

# from common.services.log_service import LogService
from common.services.components.logger import get_logger

binary_number_spaces = ['　', ' ']
env = environ.Env()
env.read_env('env/pc.env')


class CommonService:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.FILE_PATH_BASE = os.path.abspath(os.curdir)
        self.FILE_PATH_STOCK = self.FILE_PATH_BASE + '/stock'
        self.PC_NAME = env('PC_NAME')

    def get_logger(self, logger=None, filename="logger.log", is_rotate=True):
        return get_logger(filename=filename, is_rotate=is_rotate) if logger is None else logger

    def get_timezone(self):
        return timezone(timedelta(hours=+9), 'JST')

    def encode_space_identifier(self, number, start='', end=''):
        space_identifier = ''
        for num in bin(number)[2:]:
            space_identifier += binary_number_spaces[int(num)]
        return start + space_identifier + end

    def decode_space_identifier(self, space_identifier, start='', end=''):
        number = ''
        space_identifier = re.sub('^' + start, '', space_identifier)
        space_identifier = re.sub(end + '$', '', space_identifier)
        for space in space_identifier:
            number += str(binary_number_spaces.index(space))
        try:
            return int('0b' + number, 2)
        except Exception as e:
            return None

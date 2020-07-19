import logging
from datetime import datetime

# Constants
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class Logger:
    def __init__(self, filename: str, debug: bool = True):
        self._filename = filename
        self._log = logging.getLogger('file-logger')
        if debug:
            self._level = logging.DEBUG
        else:
            self._level = logging.INFO
        self._log.setLevel(self._level)
        self._handler = logging.FileHandler(filename)
        self._handler.setFormatter(formatter)
        self._log.addHandler(self._handler)

    def info(self, msg: str):
        dt = datetime.now()
        print(f'[{dt}] - {self._filename} - INFO - {msg}')
        self._log.info(msg)

    def warn(self, msg: str):
        dt = datetime.now()
        print(f'[{dt}] - {self._filename} - WARN - {msg}')
        self._log.warn(msg)

    def error(self, msg: str):
        dt = datetime.now()
        print(f'[{dt}] - {self._filename} - ERROR - {msg}')
        self._log.error(msg)

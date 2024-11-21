from os import getenv
from core.api import API
from dotenv import load_dotenv
load_dotenv()

from lib.logger import logging as log
from core import server

if __name__ == "__main__":
    server.start()

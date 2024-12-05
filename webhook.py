from core.server import start
from lib.logger import logging as log

if __name__ == "__main__":
    log.info("Service WEBHOOK is starting...")
    start()
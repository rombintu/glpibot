from lib.logger import logging as log
import asyncio
from telegram import api


if __name__ == "__main__":
    log.info("Service TELEGRAM BOT is starting...")
    asyncio.run(api.start_bot_async(), debug=False)



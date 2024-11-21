import asyncio, os, sys
from aiogram import Bot
from lib.logger import logging as log
# from aiogram.enums.parse_mode import ParseMode as pm

token = os.getenv("BOT_TOKEN")
chid = os.getenv("BOT_CHANNEL_ID")

if not token or not chid:
    log.error("BOT_TOKEN or BOT_CHANNEL_ID are not set")
    sys.exit(0)
else:
    log.debug(f"load env\n\tTOKEN {token}\n\tCHAT {chid}")

bot = Bot(token=token)

async def simple_send_message(chid: int | str, content: str):
    await bot.send_message(chid, content) 
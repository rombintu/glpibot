import asyncio, os, sys
from aiogram import Bot, Dispatcher, types
from lib.logger import logging as log
# from aiogram.enums.parse_mode import ParseMode as pm
from telegram.routes import report
from aiogram.client.bot import DefaultBotProperties
from dotenv import load_dotenv
load_dotenv()

token = os.getenv("BOT_TOKEN")
chid = os.getenv("BOT_CHANNEL_ID")

if not token or not chid:
    log.error("BOT_TOKEN or BOT_CHANNEL_ID are not set")
    sys.exit(0)
else:
    log.debug(f"load env\n\tTOKEN {token}\n\tCHAT {chid}")

bot = Bot(token, default=DefaultBotProperties(link_preview_is_disabled=True))
dp = Dispatcher()
dp.include_router(report.router)

async def simple_send_message(chid: int | str, content: str):
    await bot.send_message(chid, content)

async def setup_bot_commands():
    bot_commands = [
        types.BotCommand(command="/report", description="SLA Выгрузить отчет"),       
    ]
    await bot.set_my_commands(bot_commands)

async def start_bot_async():
    log.info("Bot is starting...")
    await setup_bot_commands()
    await dp.start_polling(bot)

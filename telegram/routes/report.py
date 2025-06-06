from aiogram import Router, F, types
from aiogram.filters.command import Command
# from aiogram.fsm.context import FSMContext
from core.api import API
from lib.helper import new_report_file
from os import getenv
import time

router = Router()
REPORT_FILE_PATH = "/tmp/report.csv"

@router.message(Command('report'))
async def handle_command_stats(message: types.Message):
    await message.answer("Отчет подготавливается...")
    start_report_time = time.time()

    app_token = getenv("APP_TOKEN")
    user_token = getenv("USER_TOKEN")
    url = getenv("SERVICE_URL")
    api_endpoint = getenv("API_ENDPOINT")
    api = API(url=url+api_endpoint, app_token=app_token, user_token=user_token)

    tickets = api.get_tickets()
    slas = api.get_slas()
    categories = api.get_categories()
    report = api.prepare_report(tickets, slas, categories)
    new_report_file(report, pathfile=REPORT_FILE_PATH)

    stop_report_time = time.time()
    await message.answer_document(
        types.input_file.FSInputFile(REPORT_FILE_PATH, filename=REPORT_FILE_PATH),
        caption=f"Отчет готов за {round(stop_report_time-start_report_time, 2)} сек.")
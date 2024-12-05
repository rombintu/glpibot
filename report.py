from os import getenv
from core.api import API
from dotenv import load_dotenv
from lib.helper import new_report_file
load_dotenv()



if __name__ == "__main__":
    app_token = getenv("APP_TOKEN")
    user_token = getenv("USER_TOKEN")
    url = getenv("SERVICE_URL")
    api = API(url=url, app_token=app_token, user_token=user_token)

    tickets = api.get_tickets()
    slas = api.get_slas()
    categories = api.get_categories()
    report = api.prepare_report(tickets, slas, categories)
    new_report_file(report)
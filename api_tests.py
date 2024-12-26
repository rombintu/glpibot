from core.api import API
import unittest
from os import getenv
from lib.logger import logging as log
from datetime import datetime

from lib.models.ticket import TicketOrigin

app_token = getenv("APP_TOKEN")
api_endpint = getenv("API_ENDPOINT")
user_token = getenv("USER_TOKEN")
url = getenv("SERVICE_URL")
api = API(url=url+api_endpint, app_token=app_token, user_token=user_token)

class TestApi(unittest.TestCase):
    def test_create_ticket(self):
        ticket = TicketOrigin(
            name="TEST11", content="ticket from testing", status=1, 
            priority=3, waiting_duration=0, close_delay_stat=0,
            solve_delay_stat=0, takeintoaccount_delay_stat=0,
            sla_waiting_duration=0,
            )
        ticket.set_author_id(8)
        payload = api.create_ticket(ticket.model_dump())
        log.debug(payload)

    def test_get_user(self):
        user = api.get_user(99)
        log.debug(user)

if __name__ == "__main__":
    unittest.main()
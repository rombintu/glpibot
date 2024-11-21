import glpi_api
from lib.logger import logging as log
from lib.helper import item_types
import json

class API:
    version = None
    def __init__(self, url, app_token, user_token):
        self.url = url
        self.app_token = app_token
        self.user_token = user_token
    
    def startup(self):
        try:
            with glpi_api.connect(self.url, self.app_token, self.user_token, verify_certs=False) as glpi:
                self.version = glpi.get_config().get("cfg_glpi").get('version')
        except glpi_api.GLPIError as err:
            log.error(str(err))

    def load_tasks(self):
        try:
            with glpi_api.connect(self.url, self.app_token, self.user_token, verify_certs=False) as glpi:
                tickets = glpi.get_all_items(item_types.ticket)
                with open("tickets.json", "w") as file:
                    file.write(json.dumps(tickets, indent=4))
        except glpi_api.GLPIError as err:
            log.error(str(err))


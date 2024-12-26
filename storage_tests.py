import unittest
from storage.storage import InMemStorage
import os

from lib.models.user import UserStorage
from lib.logger import logging as log
from dotenv import load_dotenv

load_dotenv()

storage = InMemStorage("users.yaml")

class TestStorage(unittest.TestCase):
    def test_save_load(self):
        log.debug(storage.users)
        storage.save()
        storage.load()
        log.debug(storage.users)

    def test_add_user(self):
        log.debug(storage.users)
        storage.add_user(UserStorage(id=1, name="1", telegram_id=1))
        storage.add_user(UserStorage(id=2, name="2", telegram_id=2))
        storage.add_user(UserStorage(id=3, name="3", telegram_id=1))

if __name__ == "__main__":
    unittest.main()
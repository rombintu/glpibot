from lib.logger import logging as log
from lib.models.user import UserStorage

import yaml

class InMemStorage:
    path = "users.yaml"
    users = {}

    def __init__(self, path="users.yaml"):
        self.path = path
        self.load()

    def save(self):
        with open(self.path, "w") as f:
            yaml.safe_dump(self.users, f)

    def load(self):
        try:
            with open(self.path) as f:
                self.users = yaml.safe_load(f)
        except Exception as err:
            log.error(err)

    def add_user(self, user: UserStorage):
        self.users.update({user.telegram_id: user.model_dump()})
        self.save()

    def get_user(self, telegram_id: int):
        user: UserStorage = self.users.get(telegram_id)
        if user:
            return UserStorage(**user)
        else:
            return None
import unittest
from lib.logger import logging as log
from core.postapi import postapi


class TestPostMail(unittest.TestCase):
    def test_post_mail(self):
        log.debug(postapi)
        login = "rnikolskiy"
        from_login = "cloudesk@at-consulting.ru"
        code = 123
        post_message = postapi.build_postmail_message(
        "Авторизация в системе Cloudesk", f"Код авторизации: <b>{code}</b><br><br><br>Сообщение сгенерированно автоматически",
        f"{login}@phoenixit.ru", from_login, True)
        error = postapi.send_email(f"{login}@at-consulting.ru", post_message, from_login)
        log.error(error)

if __name__ == "__main__":
    unittest.main()
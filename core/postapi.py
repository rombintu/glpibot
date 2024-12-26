from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl
from lib.logger import logging as log
from os import getenv
from dotenv import load_dotenv

load_dotenv()

class PostMail:
    def __init__(self):
        self.smtp_login = getenv("SMTP_LOGIN")
        self.smtp_sender = getenv("SMTP_SENDER")
        self.smtp_password = getenv("SMTP_PASSWORD")
        self.smtp_host = getenv("SMTP_HOST")
        self.smtp_port = getenv("SMTP_PORT", 587)
        # Create a secure SSL context
        self.context = ssl.create_default_context()

    def __str__(self):
        return (f"{self.smtp_login}@{self.smtp_host}:{self.smtp_port}")

    @staticmethod
    def build_postmail_message(subject, body, to_addr, from_addr, is_html=False):
        message = MIMEMultipart()
        message["From"] = from_addr
        message["To"] = to_addr
        message["Subject"] = subject
        message.attach(MIMEText(body, "html" if is_html else "plain"))

        return message.as_string()

    def send_email(self, to_addr: str, builded_message: str, from_addr):
        # Try to log in to server and send email
        try:
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.ehlo() # Can be omitted
            server.starttls(context=self.context) # Secure the connection
            server.ehlo() # Can be omitted
            server.login(self.smtp_login, self.smtp_password)
            
            error = server.sendmail(from_addr, to_addr, builded_message)
            log.warning(f"Post send mail. Errors: {error}")
        except Exception as err:
            log.error(err)
            return err
        finally:
            server.quit()
        return 0
    
postapi = PostMail()
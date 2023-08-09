import smtplib
import os
from typing import Sequence
from enum import Enum
from contextlib import suppress

from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

USER_EMAIL = os.getenv("USER_EMAIL")
PWD_EMAIL = os.getenv("PWD_EMAIL")
SERVER_EMAIL = os.getenv("SERVER_EMAIL")
PORT_EMAIL = os.getenv("PORT_EMAIL")
ENCRYPTION_METHOD = os.getenv("ENCRYPTION_METHOD")

class EncryptionMethodEnum(Enum):
    STARTTLS = 0
    SSL = 1

async def send_mail(
    receivers: Sequence[str],
    msg: MIMEMultipart,
) -> bool:
    user_mail = "" if USER_EMAIL is None else USER_EMAIL
    pwd = "" if PWD_EMAIL is None else PWD_EMAIL
    server_mail = "" if SERVER_EMAIL is None else SERVER_EMAIL
    port = 0 if PORT_EMAIL is None else int(PORT_EMAIL)
    encryption_method = None

    with suppress(KeyError):
        encryption_method = EncryptionMethodEnum.__getitem__(ENCRYPTION_METHOD)

    if encryption_method is EncryptionMethodEnum.SSL:
        with smtplib.SMTP_SSL(server_mail, port) as server:
            server.login(user_mail, pwd)
            server.sendmail(user_mail, receivers, msg.as_string())

    else:
        with smtplib.SMTP(server_mail, port) as server:
            if encryption_method is EncryptionMethodEnum.STARTTLS:
                server.starttls()
            server.login(user_mail, pwd)
            server.sendmail(user_mail, receivers, msg.as_string())



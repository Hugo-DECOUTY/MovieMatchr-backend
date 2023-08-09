import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

from adminplatform.utils.mail.build_content_new_local_admin import build_content_new_local_admin

load_dotenv()

USER_EMAIL = os.getenv("USER_EMAIL")
PWD_EMAIL = os.getenv("PWD_EMAIL")
SERVER_EMAIL = os.getenv("SERVER_EMAIL")
PORT_EMAIL = os.getenv("PORT_EMAIL")
ENCRYPTION_METHOD = os.getenv("ENCRYPTION_METHOD")

async def build_email_new_local_admin(user: dict, new_password: str) -> MIMEMultipart:
    msg = MIMEMultipart()
    msg["Subject"] = "New account : Local Administrator"
    msg["From"] = f"MicroPort CRM <{USER_EMAIL}>"
    msg["To"] = f"{user['email']}"
    msg["Reply-To"] = f"{user['email']}"
    msg.add_header("Content-Type", "text/html")

    html = await build_content_new_local_admin(f"{user['firstname']} {user['lastname']}", user["email"], new_password)

    content = MIMEText(html, "html")
    msg.attach(content)

    return msg


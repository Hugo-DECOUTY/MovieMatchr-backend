import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

from moviematchr.utils.mail.build_content_licence_already_used import build_content_licence_already_used
from moviematchr.schemas.orders.info_post_orders import UsersDict

load_dotenv()

USER_EMAIL = os.getenv("USER_EMAIL")
PWD_EMAIL = os.getenv("PWD_EMAIL")
SERVER_EMAIL = os.getenv("SERVER_EMAIL")
PORT_EMAIL = os.getenv("PORT_EMAIL")
ENCRYPTION_METHOD = os.getenv("ENCRYPTION_METHOD")

async def build_email_licence_already_used(user: UsersDict) -> MIMEMultipart:
    msg = MIMEMultipart()
    msg["Subject"] = "Licence already used"
    msg["From"] = f"MicroPort CRM <{USER_EMAIL}>"
    msg["To"] = f"{user.email}"
    msg["Reply-To"] = f"{user.email}"
    msg.add_header("Content-Type", "text/html")

    html = await build_content_licence_already_used(f"{user.firstname} {user.lastname}", user.email)

    content = MIMEText(html, "html")
    msg.attach(content)

    return msg


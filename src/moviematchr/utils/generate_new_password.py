import random
import string
import secrets
from dotenv import load_dotenv

load_dotenv()

symbols = ['*', '!', '@', '#', '$', '%', '^', '&', '(', ')', '-', '_', '+', '=', '[', ']', '{', '}', ';', '<', '>', '?', '/']

async def generate_new_password() -> str:
    new_password = ""
    new_password += secrets.choice(string.ascii_uppercase)
    new_password += secrets.choice(string.ascii_lowercase)
    new_password += secrets.choice(string.digits)
    new_password += secrets.choice(symbols)
    new_password += ''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits + ''.join(symbols)) for _ in range(4))
    new_password = ''.join(random.sample(new_password, len(new_password)))
    return new_password
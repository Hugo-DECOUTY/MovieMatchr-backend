import os
import httpx
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from os import getenv

from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

TOKEN_URL = os.getenv("TOKEN_URL")
REALM_URL = os.getenv("REALM_URL")

ADMIN_ACCOUNT_CLIENT = os.getenv("ADMIN_ACCOUNT_CLIENT")
ADMIN_ACCOUNT_CLIENT_SECRET = os.getenv("ADMIN_ACCOUNT_CLIENT_SECRET")

client = BackendApplicationClient(client_id=ADMIN_ACCOUNT_CLIENT)
oauth = OAuth2Session(client=client)

async def get_user_from_keycloak_by_email(email: str):
    token = oauth.fetch_token(
        token_url=TOKEN_URL,
        client_id=ADMIN_ACCOUNT_CLIENT,
        client_secret=ADMIN_ACCOUNT_CLIENT_SECRET,
    )
    async with httpx.AsyncClient() as client_async:
        user = await client_async.get(
            f"{REALM_URL}/users",
            headers={"Authorization": f"Bearer {token['access_token']}"},
            params={
                "email": f"{email}",
                "exact": True,
            },
        )

    if user.status_code != 200:
        raise HTTPException(status_code=user.status_code)

    return user.json()
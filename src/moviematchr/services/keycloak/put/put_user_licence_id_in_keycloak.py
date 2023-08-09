from os import getenv

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from fastapi import HTTPException

import httpx

TOKEN_URL = getenv("TOKEN_URL")
ADMIN_ACCOUNT_CLIENT = getenv("ADMIN_ACCOUNT_CLIENT")
ADMIN_ACCOUNT_CLIENT_SECRET = getenv("ADMIN_ACCOUNT_CLIENT_SECRET")
REALM_URL = getenv("REALM_URL")

client = BackendApplicationClient(client_id=ADMIN_ACCOUNT_CLIENT)
oauth = OAuth2Session(client=client)

async def put_user_licence_id_in_keycloak(user_id: str):
    token = oauth.fetch_token(
        token_url=TOKEN_URL,
        client_id=ADMIN_ACCOUNT_CLIENT,
        client_secret=ADMIN_ACCOUNT_CLIENT_SECRET,
    )
    async with httpx.AsyncClient() as client_async:
        response = await client_async.put(
            f"{REALM_URL}/users/{user_id}",
            headers={"Authorization": f"Bearer {token['access_token']}"},
            json={
                "attributes": {"licence_id": ""},
            },
        )
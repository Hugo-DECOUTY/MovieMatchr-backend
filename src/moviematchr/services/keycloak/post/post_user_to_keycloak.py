import os
import httpx
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from os import getenv

from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
TOKEN_URL = os.getenv("TOKEN_URL")
AUTH_URL = os.getenv("AUTH_URL")
REALM_URL = os.getenv("REALM_URL")

DOCTOR_GROUP_ID = getenv("DOCTOR_GROUP_ID")
MEDICAL_STAFF_GROUP_ID = getenv("MEDICAL_STAFF_GROUP_ID")
NON_MEDICAL_STAFF_GROUP_ID = getenv("NON_MEDICAL_STAFF_GROUP_ID")
HDS_LOCAL_ADMIN_GROUP_ID = getenv("HDS_LOCAL_ADMIN_GROUP_ID")

ADMIN_ACCOUNT_REALM = os.getenv("ADMIN_ACCOUNT_REALM")
ADMIN_ACCOUNT_CLIENT = os.getenv("ADMIN_ACCOUNT_CLIENT")
ADMIN_ACCOUNT_CLIENT_SECRET = os.getenv("ADMIN_ACCOUNT_CLIENT_SECRET")

client = BackendApplicationClient(client_id=ADMIN_ACCOUNT_CLIENT)
oauth = OAuth2Session(client=client)

async def post_user_to_keycloak(first_name: str, last_name: str, email: str, password: str):
    token = oauth.fetch_token(
        token_url=TOKEN_URL,
        client_id=ADMIN_ACCOUNT_CLIENT,
        client_secret=ADMIN_ACCOUNT_CLIENT_SECRET,
    )

    async with httpx.AsyncClient() as client_async:
        response = await client_async.post(
            f"{REALM_URL}/users",
            headers={"Authorization": f"Bearer {token['access_token']}"},
            json={
                "firstName": f"{first_name}",
                "lastName": f"{last_name}",
                "email": f"{email}",
                "enabled": True,
                "requiredActions": ["CONFIGURE_TOTP", "VERIFY_EMAIL", "TERMS_AND_CONDITIONS"],
                "credentials":[{"type":"password", "value": f"{password}", "temporary": True}],
            },
        )

    if response.status_code != 201:
        raise HTTPException(status_code=response.status_code)

    return True

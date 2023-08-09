import os
import httpx
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

BASE_URL = os.getenv("BASE_URL")
TOKEN_URL = os.getenv("TOKEN_URL")
AUTH_URL = os.getenv("AUTH_URL")
REALM_URL = os.getenv("REALM_URL")

ADMIN_ACCOUNT_REALM = os.getenv("ADMIN_ACCOUNT_REALM")
ADMIN_ACCOUNT_CLIENT = os.getenv("ADMIN_ACCOUNT_CLIENT")
ADMIN_ACCOUNT_CLIENT_SECRET = os.getenv("ADMIN_ACCOUNT_CLIENT_SECRET")

client = BackendApplicationClient(client_id=ADMIN_ACCOUNT_CLIENT)
oauth = OAuth2Session(client=client)

async def put_user_to_keycloak(
        user_id: str,
        first_name: str,
        last_name: str,
        email: str,
        licence_id: str = "",
        resetRequiredActions: bool = False,
        is_otp: bool = False,
        linked_account: str = None,
    ):

    token = oauth.fetch_token(
        token_url=TOKEN_URL,
        client_id=ADMIN_ACCOUNT_CLIENT,
        client_secret=ADMIN_ACCOUNT_CLIENT_SECRET,
    )
    dico = {
        "attributes": {"licence_id": f"{licence_id}"},
        "firstName": f"{first_name}",
        "lastName": f"{last_name}",
        "email": f"{email}",
    }
    if(linked_account) :
        dico["attributes"]["linked_account"] = linked_account

    if(licence_id == ""):
        dico.pop("attributes")

    if(resetRequiredActions):
        if is_otp:
            dico["requiredActions"] = ["CONFIGURE_TOTP", "VERIFY_EMAIL", "TERMS_AND_CONDITIONS"]
        else:
            dico["requiredActions"] = ["VERIFY_EMAIL", "TERMS_AND_CONDITIONS"]

    async with httpx.AsyncClient() as client_async:
        response = await client_async.put(
            f"{REALM_URL}/users/{user_id}",
            headers={"Authorization": f"Bearer {token['access_token']}"},
            json=dico,
        )

    if response.status_code != 204:
        raise HTTPException(status_code=response.status_code)


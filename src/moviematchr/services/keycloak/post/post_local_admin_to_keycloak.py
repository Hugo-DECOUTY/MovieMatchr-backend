from fastapi import HTTPException
from os import getenv
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import httpx

TOKEN_URL = getenv("TOKEN_URL")
ADMIN_ACCOUNT_CLIENT = getenv("ADMIN_ACCOUNT_CLIENT")
ADMIN_ACCOUNT_CLIENT_SECRET = getenv("ADMIN_ACCOUNT_CLIENT_SECRET")
REALM_URL = getenv("REALM_URL")

DOCTOR_GROUP_ID = getenv("DOCTOR_GROUP_ID")
MEDICAL_STAFF_GROUP_ID = getenv("MEDICAL_STAFF_GROUP_ID")
NON_MEDICAL_STAFF_GROUP_ID = getenv("NON_MEDICAL_STAFF_GROUP_ID")
HDS_LOCAL_ADMIN_GROUP_ID = getenv("HDS_LOCAL_ADMIN_GROUP_ID")

client = BackendApplicationClient(client_id=ADMIN_ACCOUNT_CLIENT)
oauth = OAuth2Session(client=client)

async def post_local_admin_to_keycloak(email: str, firstname: str, lastname: str, password: str):
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
                "firstName": f"{firstname}",
                "lastName": f"{lastname}",
                "email": f"{email}",
                "enabled": True,
                "requiredActions": ["CONFIGURE_TOTP", "VERIFY_EMAIL", "TERMS_AND_CONDITIONS"],
                "credentials":[{"type":"password","value": f"{password}","temporary": True}],
            },
        )
    if response.status_code != 201:
        raise HTTPException(status_code=response.status_code, detail="Local admin not created in keycloak")

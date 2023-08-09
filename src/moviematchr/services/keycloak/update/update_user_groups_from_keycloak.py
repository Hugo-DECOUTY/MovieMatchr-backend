import os
import httpx
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from os import getenv

from dotenv import load_dotenv
from fastapi import HTTPException
from moviematchr.schemas.licences.licences import TypeLicenceEnum

load_dotenv()

TOKEN_URL = os.getenv("TOKEN_URL")
REALM_URL = os.getenv("REALM_URL")

MICROPORT_STAFF_GROUP_ID = getenv("MICROPORT_STAFF_GROUP_ID")
DOCTOR_GROUP_ID = getenv("DOCTOR_GROUP_ID")
MEDICAL_STAFF_GROUP_ID = getenv("MEDICAL_STAFF_GROUP_ID")
NON_MEDICAL_STAFF_GROUP_ID = getenv("NON_MEDICAL_STAFF_GROUP_ID")
HDS_LOCAL_ADMIN_GROUP_ID = getenv("HDS_LOCAL_ADMIN_GROUP_ID")

ADMIN_ACCOUNT_CLIENT = os.getenv("ADMIN_ACCOUNT_CLIENT")
ADMIN_ACCOUNT_CLIENT_SECRET = os.getenv("ADMIN_ACCOUNT_CLIENT_SECRET")

client = BackendApplicationClient(client_id=ADMIN_ACCOUNT_CLIENT)
oauth = OAuth2Session(client=client)


async def update_user_groups_from_keycloak(user_id: str, group_id: int):
    token = oauth.fetch_token(
        token_url=TOKEN_URL,
        client_id=ADMIN_ACCOUNT_CLIENT,
        client_secret=ADMIN_ACCOUNT_CLIENT_SECRET,
    )
    if group_id == TypeLicenceEnum.DOCTOR.value:
        async with httpx.AsyncClient() as client_async:
            response = await client_async.put(
                f"{REALM_URL}/users/{user_id}/groups/{DOCTOR_GROUP_ID}",
                headers={"Authorization": f"Bearer {token['access_token']}"},
            )

            if response.status_code != 204:
                raise HTTPException(
                    response.status_code, detail="User not updated in keycloak (DOCTOR)"
                )

    elif group_id == TypeLicenceEnum.MICROPORT_STAFF.value:
        async with httpx.AsyncClient() as client_async:
            response = await client_async.put(
                f"{REALM_URL}/users/{user_id}/groups/{MICROPORT_STAFF_GROUP_ID}",
                headers={"Authorization": f"Bearer {token['access_token']}"},
            )

            if response.status_code != 204:
                raise HTTPException(
                    response.status_code,
                    detail="User not updated in keycloak (MICROPORT STAFF)",
                )

    elif group_id == TypeLicenceEnum.MEDICAL_STAFF.value:
        async with httpx.AsyncClient() as client_async:
            response = await client_async.put(
                f"{REALM_URL}/users/{user_id}/groups/{MEDICAL_STAFF_GROUP_ID}",
                headers={"Authorization": f"Bearer {token['access_token']}"},
            )

            if response.status_code != 204:
                raise HTTPException(
                    response.status_code,
                    detail="User not updated in keycloak (MEDICAL STAFF)",
                )

    elif group_id == TypeLicenceEnum.NON_MEDICAL_STAFF.value:
        async with httpx.AsyncClient() as client_async:
            response = await client_async.put(
                f"{REALM_URL}/users/{user_id}/groups/{NON_MEDICAL_STAFF_GROUP_ID}",
                headers={"Authorization": f"Bearer {token['access_token']}"},
            )

            if response.status_code != 204:
                raise HTTPException(
                    response.status_code,
                    detail="User not updated in keycloak (NON MEDICAL STAFF)",
                )

    elif group_id == TypeLicenceEnum.HDS_LOCAL_ADMIN.value:
        async with httpx.AsyncClient() as client_async:
            response = await client_async.put(
                f"{REALM_URL}/users/{user_id}/groups/{HDS_LOCAL_ADMIN_GROUP_ID}",
                headers={"Authorization": f"Bearer {token['access_token']}"},
            )

            if response.status_code != 204:
                raise HTTPException(
                    response.status_code,
                    detail="User not updated in keycloak (HDS LOCAL ADMIN)",
                )
    else:
        raise HTTPException(status_code=400, detail="Group not found")

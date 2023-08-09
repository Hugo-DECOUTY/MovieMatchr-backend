import base64
from enum import Enum
import json

from fastapi import HTTPException

# Get the payload of an access token
def get_payload(token: str):
    if "." in token:
        payload_encoded = token.split(".")[1]
    else:
        payload_encoded = token
    payload_decoded = json.loads(
        base64.b64decode(payload_encoded + ((4 - (len(payload_encoded) % 4)) * "="))
        .decode("utf8")
        .replace("'", '"')
    )

    return payload_decoded


class UserGroup(Enum):
    LOCAL_ADMIN = 0
    HDS_ADMIN_MICROPORT = 1
    MICROPORT_STAFF = 2


# Get the user's group
def identify_user(groups: dict):
    if "/easyweb/roles/hds_admin_microport" in groups:
        return UserGroup.HDS_ADMIN_MICROPORT.value
    # if "/easyweb/roles/microport_staff" in groups:
    #     return UserGroup.MICROPORT_STAFF.value
    if "/easyweb/roles/local_admin" in groups:
        return UserGroup.LOCAL_ADMIN.value

    raise HTTPException(status_code=403)


def get_payload_and_groups(token: str):
    payload = get_payload(token)
    groups = identify_user(payload["groups"])
    return payload, groups

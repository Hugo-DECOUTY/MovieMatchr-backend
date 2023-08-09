from fastapi import HTTPException, Request

from adminplatform.enum.errors.HttpErrorsEnum import HttpErrorsEnum

from adminplatform.schemas.account.get_account import (
    GetAccount,
)

from adminplatform.utils.user_group import (
    get_payload_and_groups,
    UserGroup,
)

from adminplatform.services.keycloak.get.get_user_from_keycloak_by_id import (
    get_user_from_keycloak_by_id,
)


async def get_account(request: Request, id_user: str) -> GetAccount:

    _, group = get_payload_and_groups(request.headers.get("X-USERINFO"))

    if group in (
        UserGroup.HDS_ADMIN_MICROPORT.value,
        UserGroup.LOCAL_ADMIN.value,
    ):

        response = await get_user_from_keycloak_by_id(id_user)

        if response.status_code == 404:
            raise HTTPException(
                status_code=404, detail=HttpErrorsEnum.USER_NOT_FOUND.value
            )

        response = response.json()

        return GetAccount(
            id=response["id"],
            email=response["email"],
            first_name=response["firstName"],
            last_name=response["lastName"],
        )

    raise HTTPException(status_code=403)

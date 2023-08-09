from typing import Sequence
from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from moviematchr.enum.errors.HttpErrorsEnum import HttpErrorsEnum

from moviematchr.schemas.orders.orders import Orders
from moviematchr.schemas.licences.licences import Licences
from moviematchr.schemas.account.user import Type2FA

from moviematchr.services.orders import get_order_dal
from moviematchr.services.licences import get_licences_from_order_dal
from moviematchr.services.keycloak.get.get_user_from_keycloak_by_id import (
    get_user_from_keycloak_by_id,
)
from moviematchr.services.keycloak.get.get_user_credentials import (
    get_user_credentials,
)

from moviematchr.utils.user_group import UserGroup, get_payload_and_groups


async def get_users_from_order(
    db: AsyncSession,
    request: Request,
    order_id: str,
):
    payload, group = get_payload_and_groups(request.headers.get("X-USERINFO"))

    if group in (
        UserGroup.HDS_ADMIN_MICROPORT.value,
        UserGroup.LOCAL_ADMIN.value,
    ):

        order: Orders = await get_order_dal(db, order_id)

        if order is None:
            raise HTTPException(
                status_code=404, detail=HttpErrorsEnum.ORDER_NOT_FOUND.value
            )

        if (
            str(order.local_admin_id) != payload["sub"]
            and group == UserGroup.LOCAL_ADMIN.value
        ):
            raise HTTPException(status_code=403)

        licences: Sequence[Licences] = await get_licences_from_order_dal(db, order.id)

        users: Sequence[dict] = []

        for licence in licences:

            if licence.id_user is not None:
                user = await get_user_from_keycloak_by_id(str(licence.id_user))

                if user.status_code == 200:
                    user = user.json()

                    response = await get_user_credentials(str(licence.id_user))

                    if response.status_code == 404:
                        raise HTTPException(
                            status_code=404, detail=HttpErrorsEnum.USER_NOT_FOUND.value
                        )

                    response = response.json()

                    is_mobile_app = False

                    for credential in response:
                        if credential["type"] == "otp":
                            is_mobile_app = True
                            break

                    if is_mobile_app:
                        users.append(
                            {
                                "type_2fa": Type2FA.MOBILE_APP.value,
                                "licence_type": licence.licence_type,
                                "email": user["email"],
                                "firstname": user["firstName"],
                                "lastname": user["lastName"],
                            }
                        )
                    else:
                        users.append(
                            {
                                "type_2fa": Type2FA.EMAIL.value,
                                "licence_type": licence.licence_type,
                                "email": user["email"],
                                "firstname": user["firstName"],
                                "lastname": user["lastName"],
                            }
                        )

        return users

    raise HTTPException(status_code=403)

from typing import Sequence

from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from moviematchr.enum.errors.HttpErrorsEnum import HttpErrorsEnum

from moviematchr.schemas.orders.orders import Orders
from moviematchr.schemas.licences.licences import Licences
from moviematchr.schemas.sellers.sellers import Sellers
from moviematchr.schemas.account.user import Type2FA

from moviematchr.services.orders import get_order_dal
from moviematchr.services.licences import get_licences_from_order_dal
from moviematchr.services.sellers import get_seller_dal
from moviematchr.services.keycloak.get.get_user_from_keycloak_by_id import (
    get_user_from_keycloak_by_id,
)
from moviematchr.services.keycloak.get.get_user_credentials import (
    get_user_credentials,
)

from moviematchr.utils.user_group import UserGroup, get_payload_and_groups


async def get_order_about(db: AsyncSession, request: Request, order_id: str):
    _, group = get_payload_and_groups(request.headers.get("X-USERINFO"))

    if group == UserGroup.HDS_ADMIN_MICROPORT.value:

        result = {}

        order: Orders = await get_order_dal(db, order_id)

        if order is None:
            raise HTTPException(status_code=404)

        licences: Sequence[Licences] = await get_licences_from_order_dal(db, order_id)
        seller: Sellers = await get_seller_dal(db, order.seller_id)

        local_admin = await get_user_from_keycloak_by_id(str(order.local_admin_id))

        if local_admin.status_code == 200:
            local_admin = local_admin.json()

        order_users: Sequence[dict] = []
        sum_of_recording_analyzed_in_order: int = 0
        for licence in licences:
            sum_of_recording_analyzed_in_order += licence.nb_recording_analyzed
            response = await get_user_from_keycloak_by_id(str(licence.id_user))
            if response.status_code == 200:
                response = response.json()

                response_credential = await get_user_credentials(response["id"])

                if response_credential.status_code == 404:
                    raise HTTPException(
                        status_code=404, detail=HttpErrorsEnum.USER_NOT_FOUND.value
                    )

                response_credential = response_credential.json()

                authentificator = Type2FA.EMAIL.value

                if (
                    "requiredActions" in response
                    and "CONFIGURE_TOTP" in response["requiredActions"]
                ):
                    authentificator = Type2FA.MOBILE_APP.value

                if authentificator == Type2FA.EMAIL.value:
                    for credential in response_credential:
                        if credential["type"] == "otp":
                            authentificator = Type2FA.MOBILE_APP.value
                            break

                order_users.append(
                    {
                        "type_2fa": authentificator,
                        "licence_type": licence.licence_type,
                        "id_licence": licence.id,
                        "email": response["email"],
                        "firstname": response["firstName"],
                        "lastname": response["lastName"],
                    }
                )

        result.update(
            {
                "local_admin": {
                    "email": local_admin["email"],
                    "firstname": local_admin["firstName"],
                    "lastname": local_admin["lastName"],
                },
                "users": order_users,
                "seller": {
                    "email": seller.email,
                    "firstname": seller.firstname,
                    "lastname": seller.lastname,
                    "phone": seller.phone,
                },
                "sum_of_recording_analyzed_in_order": sum_of_recording_analyzed_in_order + order.nb_shared_tokens,
            }
        )
        return result

    raise HTTPException(status_code=403)

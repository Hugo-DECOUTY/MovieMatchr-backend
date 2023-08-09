from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from moviematchr.enum.errors.HttpErrorsEnum import HttpErrorsEnum

from moviematchr.schemas.orders.orders import Orders
from moviematchr.schemas.licences.licences import Licences
from moviematchr.services.orders import get_order_dal
from moviematchr.services.licences import get_licence_dal, update_licence_dal
from moviematchr.services.keycloak.delete.delete_user_groups_from_keycloak import (
    delete_user_groups_from_keycloak,
)
from moviematchr.services.keycloak.put.put_user_licence_id_in_keycloak import (
    put_user_licence_id_in_keycloak,
)
from moviematchr.utils.user_group import UserGroup, get_payload_and_groups


async def patch_user_licence(db: AsyncSession, request: Request, id_licence: str):
    payload, group = get_payload_and_groups(request.headers.get("X-USERINFO"))

    if group in (
        UserGroup.HDS_ADMIN_MICROPORT.value,
        UserGroup.LOCAL_ADMIN.value,
    ):

        licence: Licences = await get_licence_dal(db, id_licence)

        if licence is None:
            raise HTTPException(
                status_code=404, detail=HttpErrorsEnum.LICENCE_NOT_FOUND.value
            )

        order: Orders = await get_order_dal(db, licence.id_order)

        if order is None:
            raise HTTPException(
                status_code=404, detail=HttpErrorsEnum.ORDER_NOT_FOUND.value
            )

        if group == UserGroup.LOCAL_ADMIN.value and payload["sub"] != str(
            order.local_admin_id
        ):
            raise HTTPException(
                status_code=403, detail=HttpErrorsEnum.YOU_DO_NOT_OWN_THIS_ORDER.value
            )

        await delete_user_groups_from_keycloak(
            str(licence.id_user), licence.licence_type
        )
        await put_user_licence_id_in_keycloak(str(licence.id_user))
        licence.id_user = None
        licence.licence_type = None
        await update_licence_dal(db, licence)

        return licence

    raise HTTPException(status_code=403)

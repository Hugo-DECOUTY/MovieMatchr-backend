from typing import Sequence
from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from adminplatform.enum.errors.HttpErrorsEnum import HttpErrorsEnum

from adminplatform.schemas.orders.orders import Orders
from adminplatform.schemas.licences.licences import Licences
from adminplatform.services.orders import get_order_dal
from adminplatform.services.licences import get_licences_from_order_dal
from adminplatform.utils.user_group import UserGroup, get_payload_and_groups


async def get_licences_from_order(db: AsyncSession, request: Request, id_order: str):
    payload, group = get_payload_and_groups(request.headers.get("X-USERINFO"))

    if group in (
        UserGroup.HDS_ADMIN_MICROPORT.value,
        UserGroup.LOCAL_ADMIN.value,
    ):
        order: Orders = await get_order_dal(db, id_order)

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

        licences: Sequence[Licences] = await get_licences_from_order_dal(db, id_order)

        return licences

    raise HTTPException(status_code=403)

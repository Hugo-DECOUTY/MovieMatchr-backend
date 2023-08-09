from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from adminplatform.enum.errors.HttpErrorsEnum import HttpErrorsEnum

from adminplatform.schemas.orders.orders import Orders

from adminplatform.services.orders import get_order_dal, update_order_dal

from adminplatform.utils.socket import socket_manager as sio
from adminplatform.utils.user_group import UserGroup, get_payload_and_groups


async def update_order_billing_type(
    db: AsyncSession, request: Request, order_id: str, billing_type: int
) -> dict:
    payload, group = get_payload_and_groups(request.headers.get("X-USERINFO"))
    if group == UserGroup.HDS_ADMIN_MICROPORT.value:

        order: Orders = await get_order_dal(db, order_id)

        if order is None:
            raise HTTPException(
                status_code=404, detail=HttpErrorsEnum.ORDER_NOT_FOUND.value
            )

        order.billing_type = billing_type

        await update_order_dal(db, order)
        await sio.emit("orders", room=payload["sub"])
        return {"status_code:": 204, "message": "Order billing type updated"}

    raise HTTPException(status_code=403)

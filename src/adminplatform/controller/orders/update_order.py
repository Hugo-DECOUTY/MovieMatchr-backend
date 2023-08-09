from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from adminplatform.enum.errors.HttpErrorsEnum import HttpErrorsEnum

from adminplatform.schemas.orders.orders import Orders
from adminplatform.schemas.orders.info_patch_orders import InfoPatchOrders

from adminplatform.services.orders import get_order_dal, update_order_dal

from adminplatform.utils.socket import socket_manager as sio
from adminplatform.utils.user_group import UserGroup, get_payload_and_groups

async def update_order(
    db: AsyncSession, request: Request, order_id: str, infos: InfoPatchOrders
):
    payload, group = get_payload_and_groups(request.headers.get("X-USERINFO"))
    if group == UserGroup.HDS_ADMIN_MICROPORT.value:

        order: Orders = await get_order_dal(db, order_id)

        if order is None:
            raise HTTPException(status_code=404, detail=HttpErrorsEnum.ORDER_NOT_FOUND.value)

        order.order_id = infos.order_id
        order.workplace = infos.workplace
        order.service = infos.service
        order.seller_id = infos.seller_id
        order.state_flag = infos.state_flag

        await update_order_dal(db, order)
        await sio.emit("orders", room=payload["sub"])
        return order

    raise HTTPException(status_code=403)

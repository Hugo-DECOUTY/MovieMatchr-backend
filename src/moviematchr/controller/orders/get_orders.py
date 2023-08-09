from typing import Sequence
from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from moviematchr.schemas.orders.orders import Orders

from moviematchr.services.orders import get_orders_dal

from moviematchr.utils.user_group import UserGroup, get_payload_and_groups


async def get_orders(db: AsyncSession, request: Request, state_flag: int):
    payload, group = get_payload_and_groups(request.headers.get("X-USERINFO"))

    if group == UserGroup.HDS_ADMIN_MICROPORT.value:
        orders: Sequence[Orders] = await get_orders_dal(db)
        if state_flag != -1:
            orders = [order for order in orders if order.state_flag == state_flag]

        return orders

    elif group == UserGroup.LOCAL_ADMIN.value:
        orders: Sequence[Orders] = await get_orders_dal(db)
        orders = [
            order for order in orders if str(order.local_admin_id) == payload["sub"]
        ]
        if state_flag != -1:
            orders = [order for order in orders if order.state_flag == state_flag]

        return orders

    raise HTTPException(status_code=403)

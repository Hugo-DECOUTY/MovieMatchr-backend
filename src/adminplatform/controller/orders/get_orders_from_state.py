from typing import Sequence
from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from adminplatform.schemas.orders.orders import Orders
from adminplatform.services.orders import (
    get_orders_from_state_dal,
)
from adminplatform.utils.user_group import UserGroup, get_payload_and_groups


async def get_orders_from_state(db: AsyncSession, request: Request, state_flag: int):
    _, group = get_payload_and_groups(request.headers.get("X-USERINFO"))

    if group == UserGroup.HDS_ADMIN_MICROPORT.value:
        orders: Sequence[Orders] = await get_orders_from_state_dal(db, state_flag)
        return orders

    raise HTTPException(status_code=403)

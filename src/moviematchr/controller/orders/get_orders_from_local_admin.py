from typing import Sequence
from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from moviematchr.schemas.orders.orders import Orders

from moviematchr.services.orders import (
    get_orders_from_local_admin_dal,
)

from moviematchr.utils.user_group import UserGroup, get_payload_and_groups


async def get_orders_from_user(db: AsyncSession, request: Request, local_admin_id: str):
    _, group = get_payload_and_groups(request.headers.get("X-USERINFO"))

    if group in (
        UserGroup.HDS_ADMIN_MICROPORT.value,
        UserGroup.LOCAL_ADMIN.value,
    ):
        orders: Sequence[Orders] = await get_orders_from_local_admin_dal(
            db, local_admin_id
        )

        return orders

    raise HTTPException(status_code=403)

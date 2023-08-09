from typing import Sequence
from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from adminplatform.schemas.tickets.tickets import Tickets

from adminplatform.services.tickets import (
    get_tickets_from_user_dal,
)

from adminplatform.utils.user_group import UserGroup, get_payload_and_groups


async def get_tickets_from_user(db: AsyncSession, request: Request, user: str):
    payload, group = get_payload_and_groups(request.headers.get("X-USERINFO"))

    if group == UserGroup.HDS_ADMIN_MICROPORT.value:
        tickets: Sequence[Tickets] = await get_tickets_from_user_dal(db, user)
        return tickets

    if group == UserGroup.LOCAL_ADMIN.value and user == payload["sub"]:
        tickets: Sequence[Tickets] = await get_tickets_from_user_dal(
            db, payload["sub"]
        )
        return tickets

    raise HTTPException(status_code=403)

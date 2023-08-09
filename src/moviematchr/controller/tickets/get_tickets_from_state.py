from typing import Sequence
from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from moviematchr.schemas.tickets.tickets import Tickets

from moviematchr.services.tickets import (
    get_tickets_from_user_dal,
    get_tickets_dal,
)

from moviematchr.utils.user_group import UserGroup, get_payload_and_groups


async def get_tickets_from_state(db: AsyncSession, request: Request, state_flag: int):
    payload, group = get_payload_and_groups(request.headers.get("X-USERINFO"))

    if group == UserGroup.HDS_ADMIN_MICROPORT.value:
        tickets: Sequence[Tickets] = await get_tickets_dal(db)
        tickets = [ticket for ticket in tickets if ticket.state_flag == state_flag]
        return tickets

    if group == UserGroup.LOCAL_ADMIN.value:
        tickets: Sequence[Tickets] = await get_tickets_from_user_dal(
            db, payload["sub"]
        )
        tickets = [ticket for ticket in tickets if ticket.state_flag == state_flag]
        return tickets

    raise HTTPException(status_code=403)

from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from moviematchr.enum.errors.HttpErrorsEnum import HttpErrorsEnum

from moviematchr.schemas.tickets.tickets import Tickets

from moviematchr.services.tickets import get_ticket_dal

from moviematchr.utils.user_group import UserGroup, get_payload_and_groups


async def get_ticket(db: AsyncSession, request: Request, ticket_id: str):
    payload, group = get_payload_and_groups(request.headers.get("X-USERINFO"))

    ticket: Tickets = await get_ticket_dal(db, ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail=HttpErrorsEnum.TICKET_NOT_FOUND.value
        )

    if group == UserGroup.HDS_ADMIN_MICROPORT.value:
        return ticket

    if group == UserGroup.LOCAL_ADMIN.value:

        if str(ticket.user) != payload["sub"]:
            raise HTTPException(
                status_code=403,
                detail=HttpErrorsEnum.YOU_DO_NOT_OWN_THIS_TICKET.value
            )

        return ticket

    raise HTTPException(status_code=403)

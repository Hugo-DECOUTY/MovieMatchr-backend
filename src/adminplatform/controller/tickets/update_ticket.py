from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from adminplatform.enum.errors.HttpErrorsEnum import HttpErrorsEnum

from adminplatform.schemas.tickets.tickets import Tickets, StateTicketEnum

from adminplatform.services.tickets import get_ticket_dal, update_ticket_dal

from adminplatform.utils.socket import socket_manager as sio
from adminplatform.utils.user_group import UserGroup, get_payload_and_groups
from adminplatform.utils.actual_time_in_ms import actual_time_in_ms


async def update_ticket(
    db: AsyncSession,
    request: Request,
    ticket_id: str,
    ticket_type: int,
    body: str,
    state_flag: int,
):
    payload, group = get_payload_and_groups(request.headers.get("X-USERINFO"))

    ticket: Tickets = await get_ticket_dal(db, ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=404, detail=HttpErrorsEnum.TICKET_NOT_FOUND.value
        )

    if group in (
        UserGroup.HDS_ADMIN_MICROPORT.value,
        UserGroup.LOCAL_ADMIN.value,
    ):

        if group == UserGroup.LOCAL_ADMIN.value and str(ticket.user) != payload["sub"]:
            raise HTTPException(
                status_code=403, detail=HttpErrorsEnum.YOU_DO_NOT_OWN_THIS_TICKET.value
            )

        ticket.type = ticket_type
        ticket.body = body

        if group == UserGroup.LOCAL_ADMIN.value and state_flag in (
            StateTicketEnum.DENIED.value,
            StateTicketEnum.ACCEPTED.value,
        ):
            raise HTTPException(
                status_code=403, detail=HttpErrorsEnum.TICKET_ALREADY_CLOSED.value
            )

        ticket.state_flag = state_flag

        # Update the object in the database
        ticket.update_state_date = actual_time_in_ms()
        await update_ticket_dal(db, ticket)
        await sio.emit("tickets", room=payload["sub"])
        return ticket

    raise HTTPException(status_code=403)

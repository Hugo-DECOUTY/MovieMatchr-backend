from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from adminplatform.enum.errors.HttpErrorsEnum import HttpErrorsEnum

from adminplatform.schemas.tickets.tickets import StateTicketEnum, Tickets

from adminplatform.services.tickets import delete_ticket_dal, get_ticket_dal
from adminplatform.utils.user_group import UserGroup, get_payload_and_groups


async def delete_ticket(db: AsyncSession, request: Request, ticket_id: str):
    payload, group = get_payload_and_groups(request.headers.get("X-USERINFO"))

    if group in (
        UserGroup.LOCAL_ADMIN.value,
        UserGroup.HDS_ADMIN_MICROPORT.value,
    ):
        ticket: Tickets = await get_ticket_dal(db, ticket_id)

        if ticket is None:
            raise HTTPException(
                status_code=404,
                detail=HttpErrorsEnum.TICKET_NOT_FOUND.value
            )

        if group == UserGroup.LOCAL_ADMIN.value:
            if str(ticket.user) != payload["sub"]:
                raise HTTPException(
                    status_code=403,
                    detail=HttpErrorsEnum.YOU_DO_NOT_OWN_THIS_TICKET.value,
                )

            if ticket.state_flag != StateTicketEnum.IN_PROGRESS.value:
                raise HTTPException(
                    status_code=403,
                    detail=HttpErrorsEnum.TICKET_ALREADY_CLOSED.value
                )

        await delete_ticket_dal(db, ticket_id)
        return {"message": "Ticket deleted"}

    raise HTTPException(status_code=403)

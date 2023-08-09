from typing import Sequence
from uuid import uuid4
from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from moviematchr.enum.errors.HttpErrorsEnum import HttpErrorsEnum

from moviematchr.schemas.tickets.tickets import (
    StateTicketEnum,
    Tickets,
    TypeTicketEnum,
    TicketBody,
)
from moviematchr.schemas.orders.orders import Orders
from moviematchr.schemas.licences.licences import Licences

from moviematchr.services.tickets import create_ticket_dal
from moviematchr.services.licences import get_licences_from_order_dal
from moviematchr.services.orders import get_order_dal
from moviematchr.services.keycloak.get.get_user_from_keycloak_by_email import (
    get_user_from_keycloak_by_email,
)

from moviematchr.utils.user_group import UserGroup, get_payload_and_groups
from moviematchr.utils.socket import socket_manager as sio
from moviematchr.utils.params_validation import test_email
from moviematchr.utils.actual_time_in_ms import actual_time_in_ms


async def create_ticket(
    db: AsyncSession,
    request: Request,
    id_order: str,
    ticket_type: int,
    body: TicketBody,
):
    payload, group = get_payload_and_groups(request.headers.get("X-USERINFO"))

    if group in (
        UserGroup.LOCAL_ADMIN.value,
        UserGroup.HDS_ADMIN_MICROPORT.value,
    ):
        order: Orders = await get_order_dal(db, id_order)

        if order is None:
            raise HTTPException(
                status_code=404,
                detail=HttpErrorsEnum.ORDER_NOT_FOUND.value
            )

        if (
            str(order.local_admin_id) != payload["sub"]
            and group == UserGroup.LOCAL_ADMIN.value
        ):
            raise HTTPException(
                status_code=403,
                detail=HttpErrorsEnum.YOU_DO_NOT_OWN_THIS_ORDER.value
            )

        if ticket_type == TypeTicketEnum.MODIFY_USER.value:

            licences: Sequence[Licences] = await get_licences_from_order_dal(
                db, id_order
            )
            licences_without_user = [
                licence for licence in licences if licence.id_user is None
            ]

            if len(licences_without_user) == 0:
                raise HTTPException(
                    status_code=403,
                    detail=HttpErrorsEnum.LICENCE_NOT_AVAILABLE.value
                )

            user = await get_user_from_keycloak_by_email(body["email"])

            if len(user) == 0:
                raise HTTPException(
                    status_code=404,
                    detail=HttpErrorsEnum.USER_NOT_FOUND.value
                )

            body["id"] = user[0]["id"]

            if len(body["new_email"]) == 0 or test_email(body["new_email"]) is False:
                body["new_email"] = body["email"]

        actual_time = actual_time_in_ms()

        ticket: Tickets = Tickets(
            id=str(uuid4()),
            id_order=id_order,
            user=payload["sub"],
            sending_date=actual_time,
            update_state_date=actual_time,
            type=ticket_type,
            body=body,
            state_flag=StateTicketEnum.IN_PROGRESS.value,
        )

        await create_ticket_dal(db, ticket)
        await sio.emit("tickets", room=payload["sub"])
        return ticket

    raise HTTPException(status_code=403)

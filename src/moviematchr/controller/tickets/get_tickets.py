from typing import Sequence, List
from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from moviematchr.schemas.tickets.tickets import Tickets
from moviematchr.schemas.orders.orders import Orders
from moviematchr.services.tickets import (
    get_tickets_from_user_dal,
    get_tickets_dal,
)
from moviematchr.services.orders import get_order_dal
from moviematchr.schemas.tickets.info_get_tickets import InfoGetTickets
from moviematchr.utils.user_group import UserGroup, get_payload_and_groups


async def get_tickets(
    db: AsyncSession,
    request: Request,
    user_id: str = "",
    state_flag: int = -1,
) -> List[InfoGetTickets]:
    payload, group = get_payload_and_groups(request.headers.get("X-USERINFO"))
    result: List[InfoGetTickets] = []

    if group == UserGroup.HDS_ADMIN_MICROPORT.value:
        if user_id == "":
            tickets: Sequence[Tickets] = await get_tickets_dal(db)
            if state_flag != -1:
                tickets = [
                    ticket for ticket in tickets if ticket.state_flag == state_flag
                ]
            for ticket in tickets:
                order: Orders = await get_order_dal(db, ticket.id_order)
                result.append(
                    InfoGetTickets(
                        id=ticket.id,
                        id_order=ticket.id_order,
                        order_id=order.order_id,
                        workplace=order.workplace,
                        service=order.service,
                        user=ticket.user,
                        type=ticket.type,
                        sending_date=ticket.sending_date,
                        body=ticket.body,
                        state_flag=ticket.state_flag,
                        update_state_date=ticket.update_state_date,
                    )
                )
            return result

        tickets: Sequence[Tickets] = await get_tickets_from_user_dal(db, user_id)
        if state_flag != -1:
            tickets = [ticket for ticket in tickets if ticket.state_flag == state_flag]
        for ticket in tickets:
            order: Orders = await get_order_dal(db, ticket.id_order)
            result.append(
                InfoGetTickets(
                    id=ticket.id,
                    id_order=ticket.id_order,
                    order_id=order.order_id,
                    workplace=order.workplace,
                    service=order.service,
                    user=ticket.user,
                    type=ticket.type,
                    sending_date=ticket.sending_date,
                    body=ticket.body,
                    state_flag=ticket.state_flag,
                    update_state_date=ticket.update_state_date,
                )
            )
        return result

    if group == UserGroup.LOCAL_ADMIN.value:
        if user_id == "" or user_id == payload["sub"]:
            tickets: Sequence[Tickets] = await get_tickets_from_user_dal(
                db, payload["sub"]
            )
            if state_flag != -1:
                tickets = [
                    ticket for ticket in tickets if ticket.state_flag == state_flag
                ]
            for ticket in tickets:
                order: Orders = await get_order_dal(db, ticket.id_order)
                result.append(
                    InfoGetTickets(
                        id=ticket.id,
                        id_order=ticket.id_order,
                        order_id=order.order_id,
                        workplace=order.workplace,
                        service=order.service,
                        user=ticket.user,
                        type=ticket.type,
                        sending_date=ticket.sending_date,
                        body=ticket.body,
                        state_flag=ticket.state_flag,
                        update_state_date=ticket.update_state_date,
                    )
                )
            return result

        raise HTTPException(status_code=403)

    raise HTTPException(status_code=403)

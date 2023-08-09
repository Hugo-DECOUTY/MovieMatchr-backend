from typing import Sequence
from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from adminplatform.enum.errors.HttpErrorsEnum import HttpErrorsEnum

from adminplatform.schemas.orders.orders import Orders, StateOrderEnum
from adminplatform.schemas.licences.licences import Licences
from adminplatform.schemas.tickets.tickets import Tickets

from adminplatform.services.tickets import get_tickets_from_order_dal, delete_ticket_dal
from adminplatform.services.orders import update_order_dal, get_order_dal
from adminplatform.services.licences import (
    get_licences_from_order_dal,
    delete_licence_dal,
)
from adminplatform.services.keycloak.put.put_user_licence_id_in_keycloak import (
    put_user_licence_id_in_keycloak,
)

from adminplatform.services.data_storage.delete_a_file_in_storage import (
    delete_a_file_in_storage,
)

from adminplatform.utils.user_group import UserGroup, get_payload_and_groups
from adminplatform.utils.socket import socket_manager as sio


async def delete_order(db: AsyncSession, request: Request, order_id: str):
    payload, group = get_payload_and_groups(request.headers.get("X-USERINFO"))

    if group == UserGroup.HDS_ADMIN_MICROPORT.value:

        order: Orders = await get_order_dal(db, order_id)

        if order is None:
            raise HTTPException(
                status_code=404, detail=HttpErrorsEnum.ORDER_NOT_FOUND.value
            )

        tickets: Sequence[Tickets] = await get_tickets_from_order_dal(db, order_id)
        licences: Sequence[Licences] = await get_licences_from_order_dal(db, order_id)

        for licence in licences:
            await put_user_licence_id_in_keycloak(str(licence.id_user))
            await delete_licence_dal(db, licence.id)

        for ticket in tickets:
            await delete_ticket_dal(db, ticket.id)
            await sio.emit("tickets", room=payload["sub"])

        delete_a_file_in_storage(f"{order.id}/{order.order_id}.xlsx")

        order.state_flag = StateOrderEnum.DELETED.value

        await update_order_dal(db, order)
        await sio.emit("orders", room=payload["sub"])

    else:
        raise HTTPException(status_code=403)

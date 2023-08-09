from typing import Sequence
from uuid import uuid4
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from adminplatform.enum.errors.HttpErrorsEnum import HttpErrorsEnum

from adminplatform.schemas.tickets.tickets import StateTicketEnum, Tickets, TicketBody
from adminplatform.schemas.orders.orders import Orders
from adminplatform.schemas.licences.licences import Licences
# from adminplatform.schemas.account.user import Type2FA
from adminplatform.schemas.orders.info_post_orders import UsersDict

from adminplatform.utils.user_group import UserGroup, get_payload_and_groups
from adminplatform.utils.socket import socket_manager as sio
from adminplatform.utils.actual_time_in_ms import actual_time_in_ms
from adminplatform.utils.generate_new_password import generate_new_password
from adminplatform.utils.mail.build_email_new_user import build_email_new_user
from adminplatform.utils.mail.send_mail import send_mail

from adminplatform.services.licences import get_licences_from_order_dal
from adminplatform.services.orders import get_order_dal
from adminplatform.services.keycloak.get.get_user_from_keycloak_by_email import (
    get_user_from_keycloak_by_email,
)
from adminplatform.services.keycloak.put.put_user_to_keycloak import (
    put_user_to_keycloak,
)
from adminplatform.services.keycloak.post.post_user_with_licence_to_keycloak import (
    post_user_with_licence_to_keycloak,
)
from adminplatform.services.keycloak.update.update_user_groups_from_keycloak import (
    update_user_groups_from_keycloak,
)
from adminplatform.services.licences import update_licence_dal


async def create_new_user(
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
                status_code=404, detail=HttpErrorsEnum.ORDER_NOT_FOUND.value
            )

        if (
            str(order.local_admin_id) != payload["sub"]
            and group == UserGroup.LOCAL_ADMIN.value
        ):
            raise HTTPException(status_code=403)

        id_ticket = str(uuid4())
        ticket: Tickets = Tickets(
            id=id_ticket,
            id_order=id_order,
            user=payload["sub"],
            sending_date=actual_time_in_ms(),
            type=ticket_type,
            body=body,
            state_flag=StateTicketEnum.IN_PROGRESS.value,
        )

        licences: Sequence[Licences] = await get_licences_from_order_dal(
            db, ticket.id_order
        )

        if "serial_number" in body:
            licences_without_user: Sequence[Licences] = list(
                filter(
                    lambda licence: licence.serial_number == body["serial_number"],
                    licences,
                )
            )
        else:
            licences_without_user: Sequence[Licences] = list(
                filter(lambda licence: licence.id_user is None, licences)
            )

        if len(licences_without_user) == 0:
            raise HTTPException(
                status_code=404, detail=HttpErrorsEnum.LICENCE_NOT_FOUND.value
            )

        if licences_without_user[0].id_user is not None:
            raise HTTPException(
                status_code=403, detail=HttpErrorsEnum.LICENCE_ALREADY_USED.value
            )

        licence: Licences = licences_without_user[0]

        licence.licence_type = ticket.body.licence_type

        user = await get_user_from_keycloak_by_email(ticket.body.email)

        if len(user):
            raise HTTPException(
                status_code=403, detail=HttpErrorsEnum.USER_ALREADY_EXIST.value
            )

        else:
            new_password = await generate_new_password()

            msg: MIMEMultipart = await build_email_new_user(
                UsersDict(
                    email=ticket.body.email,
                    type_2fa=ticket.body.type_2fa,
                    licence_type=ticket.body.licence_type,
                    firstname=ticket.body.firstname,
                    lastname=ticket.body.lastname,
                ),
                new_password,
            )

            await send_mail([ticket.body.email], msg)

            await post_user_with_licence_to_keycloak(
                licence.id,
                ticket.body.firstname,
                ticket.body.lastname,
                ticket.body.email,
                new_password,
            )

        new_user = await get_user_from_keycloak_by_email(ticket.body.email)

        if len(new_user) == 0:
            raise HTTPException(
                status_code=500, detail=HttpErrorsEnum.USER_CREATION_FAILED.value
            )

        licence.id_user = new_user[0]["id"]

        await put_user_to_keycloak(
            user_id=new_user[0]["id"],
            first_name=ticket.body.firstname,
            last_name=ticket.body.lastname,
            email=ticket.body.email,
            licence_id=licence.id,
            resetRequiredActions=True,
            is_otp=False,  # ticket.body.type_2fa == Type2FA.MOBILE_APP.value,
        )

        await update_user_groups_from_keycloak(
            new_user[0]["id"], ticket.body.licence_type
        )
        await update_licence_dal(db, licence)

        await sio.emit("users", room=payload["sub"])
        return {"message": "New user created"}

    raise HTTPException(status_code=403)

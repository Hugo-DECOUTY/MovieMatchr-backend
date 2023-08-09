import os
from typing import Sequence
from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from adminplatform.enum.errors.HttpErrorsEnum import HttpErrorsEnum

from adminplatform.schemas.tickets.tickets import (
    StateTicketEnum,
    Tickets,
    TypeTicketEnum,
)
from adminplatform.schemas.licences.licences import Licences, TypeLicenceEnum
from adminplatform.schemas.orders.orders import Orders
from adminplatform.schemas.orders.info_post_orders import UsersDict
from adminplatform.schemas.account.user import Type2FA

from adminplatform.services.licences import (
    get_licences_from_order_dal,
    update_licence_dal,
)
from adminplatform.services.orders import get_order_dal
from adminplatform.services.tickets import get_ticket_dal, update_ticket_dal

from adminplatform.services.keycloak.put.put_user_to_keycloak import (
    put_user_to_keycloak,
)
from adminplatform.services.keycloak.get.get_user_from_keycloak_by_email import (
    get_user_from_keycloak_by_email,
)
from adminplatform.services.keycloak.get.get_user_from_keycloak_by_id import (
    get_user_from_keycloak_by_id,
)
from adminplatform.services.keycloak.get.get_user_credentials import (
    get_user_credentials,
)
from adminplatform.services.keycloak.delete.delete_user_credentials import (
    delete_user_credentials,
)
from adminplatform.services.keycloak.delete.delete_user_groups_from_keycloak import (
    delete_user_groups_from_keycloak,
)
from adminplatform.services.keycloak.update.update_user_groups_from_keycloak import (
    update_user_groups_from_keycloak,
)

from adminplatform.utils.user_group import UserGroup, get_payload_and_groups
from adminplatform.utils.socket import socket_manager as sio
from adminplatform.utils.mail.send_mail import send_mail
from adminplatform.utils.actual_time_in_ms import actual_time_in_ms
from adminplatform.utils.mail.build_email_ticket_denied import build_email_ticket_denied

from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv

load_dotenv()

USER_EMAIL = os.getenv("USER_EMAIL")
PWD_EMAIL = os.getenv("PWD_EMAIL")
SERVER_EMAIL = os.getenv("SERVER_EMAIL")
PORT_EMAIL = os.getenv("PORT_EMAIL")
ENCRYPTION_METHOD = os.getenv("ENCRYPTION_METHOD")


async def process_ticket(
    db: AsyncSession,
    request: Request,
    ticket_id: str,
    state_flag: int,
    body: str = None,
):
    payload, group = get_payload_and_groups(request.headers.get("X-USERINFO"))

    if group == UserGroup.HDS_ADMIN_MICROPORT.value:
        ticket: Tickets = await get_ticket_dal(db, ticket_id)

        if ticket is None:
            raise HTTPException(
                status_code=404, detail=HttpErrorsEnum.TICKET_NOT_FOUND.value
            )

        if ticket.state_flag == StateTicketEnum.CANCELED.value:
            return ticket

        if state_flag in (StateTicketEnum.DENIED.value, StateTicketEnum.ACCEPTED.value):
            if ticket.state_flag != state_flag:
                ticket.update_state_date = actual_time_in_ms()

            ticket.state_flag = state_flag

            order: Orders = await get_order_dal(db, ticket.id_order)

            if order is None:
                raise HTTPException(
                    status_code=404, detail=HttpErrorsEnum.ORDER_NOT_FOUND.value
                )

            if state_flag == StateTicketEnum.ACCEPTED.value:

                if ticket.type == TypeTicketEnum.MODIFY_USER.value:
                    licences: Sequence[Licences] = await get_licences_from_order_dal(
                        db, ticket.id_order
                    )
                    user_licence = list(
                        filter(
                            lambda licence: str(licence.id_user) == ticket.body["id"],
                            licences,
                        )
                    )

                    if len(user_licence) == 0:
                        raise HTTPException(
                            status_code=400,
                            detail=HttpErrorsEnum.LICENCE_NOT_FOUND.value,
                        )

                    licence: Licences = user_licence[0]

                    if licence.licence_type != ticket.body["licence_type"]:
                        await delete_user_groups_from_keycloak(
                            ticket.body["id"], licence.licence_type
                        )
                        licence.licence_type = ticket.body["licence_type"]
                        await update_user_groups_from_keycloak(
                            ticket.body["id"], ticket.body["licence_type"]
                        )

                    is_otp = ticket.body["type_2fa"] == Type2FA.MOBILE_APP.value

                    await put_user_to_keycloak(
                        ticket.body["id"],
                        ticket.body["firstname"],
                        ticket.body["lastname"],
                        ticket.body["email"],
                        licence.id,
                        resetRequiredActions=True,
                        is_otp=is_otp,
                    )

                    new_user = await get_user_from_keycloak_by_email(
                        ticket.body["new_email"]
                    )

                    if len(new_user) == 0:
                        await put_user_to_keycloak(
                            ticket.body["id"],
                            ticket.body["firstname"],
                            ticket.body["lastname"],
                            ticket.body["new_email"],
                            licence.id,
                            resetRequiredActions=True,
                            is_otp=is_otp,
                        )

                        new_user = await get_user_from_keycloak_by_email(
                            ticket.body["new_email"]
                        )

                    licence.id_user = new_user[0]["id"]

                    if ticket.body["type_2fa"] == Type2FA.EMAIL.value:
                        response = await get_user_credentials(new_user[0]["id"])

                        if response.status_code == 404:
                            raise HTTPException(
                                status_code=404,
                                detail=HttpErrorsEnum.USER_NOT_FOUND.value,
                            )

                        response = response.json()

                        credential_id = ""

                        for credential in response:
                            if credential["type"] == "otp":
                                credential_id = credential["id"]
                                break

                        if credential_id != "":
                            await delete_user_credentials(
                                new_user[0]["id"], credential_id
                            )

                    await update_licence_dal(db, licence)

            if state_flag == StateTicketEnum.DENIED.value:
                local_admin = await get_user_from_keycloak_by_id(
                    str(order.local_admin_id)
                )
                if local_admin.status_code == 200:
                    local_admin = local_admin.json()
                    msg: MIMEMultipart = await build_email_ticket_denied(
                        UsersDict(
                            email=local_admin["email"],
                            type_2fa=Type2FA.MOBILE_APP.value,
                            licence_type=TypeLicenceEnum.HDS_LOCAL_ADMIN.value,
                            firstname=local_admin["firstName"],
                            lastname=local_admin["lastName"],
                        ),
                        body,
                    )
                    await send_mail([local_admin["email"]], msg)

            # Update the object in the database
            await update_ticket_dal(db, ticket)
            await sio.emit("tickets", room=payload["sub"])
            return ticket

    raise HTTPException(status_code=403)

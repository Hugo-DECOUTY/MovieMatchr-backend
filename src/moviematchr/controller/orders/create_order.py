from typing import Sequence
from uuid import uuid4
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from moviematchr.enum.errors.HttpErrorsEnum import HttpErrorsEnum

from moviematchr.schemas.orders.info_post_orders import InfoPostOrders
from moviematchr.schemas.orders.orders import Orders
from moviematchr.schemas.sellers.sellers import Sellers
from moviematchr.schemas.licences.licences import Licences
from moviematchr.schemas.orders.orders import StateOrderEnum
from moviematchr.schemas.orders.info_post_orders import UsersDict
from moviematchr.schemas.licences.licences import TypeLicenceEnum
from moviematchr.schemas.account.user import Type2FA

from moviematchr.services.orders import create_order_dal
from moviematchr.services.sellers import create_seller_dal, get_seller_by_email_dal
from moviematchr.services.licences import (
    create_licence_dal,
    get_licence_from_serial_dal,
)
from moviematchr.services.keycloak.get.get_user_from_keycloak_by_email import (
    get_user_from_keycloak_by_email,
)
from moviematchr.services.keycloak.get.get_user_from_keycloak_by_id import (
    get_user_from_keycloak_by_id,
)
from moviematchr.services.keycloak.update.update_user_groups_from_keycloak import (
    update_user_groups_from_keycloak,
)
from moviematchr.services.keycloak.post.post_user_with_licence_to_keycloak import (
    post_user_with_licence_to_keycloak,
)
from moviematchr.services.keycloak.put.put_user_to_keycloak import (
    put_user_to_keycloak,
)

from moviematchr.utils.user_group import UserGroup, get_payload_and_groups
from moviematchr.utils.socket import socket_manager as sio
from moviematchr.utils.actual_time_in_ms import actual_time_in_ms
from moviematchr.utils.generate_new_serial_number import generate_new_serial_number
from moviematchr.utils.generate_new_password import generate_new_password
from moviematchr.utils.mail.build_email_new_user import build_email_new_user
from moviematchr.utils.mail.build_email_licence_already_used_local_admin import (
    build_email_licence_already_used_local_admin,
)
from moviematchr.utils.mail.send_mail import send_mail
from moviematchr.controller.orders.utils.create_local_admin import create_local_admin

MAX_LICENCES = 14


async def create_order(
    db: AsyncSession,
    request: Request,
    infos: InfoPostOrders,
) -> Orders:
    payload, group = get_payload_and_groups(request.headers.get("X-USERINFO"))
    id_order = str(uuid4())

    if group == UserGroup.HDS_ADMIN_MICROPORT.value:

        # Create local admin if not exist
        local_admin_licence, local_admin_id = await create_local_admin(db, infos)

        # Create licences list
        licences: Sequence[Licences] = []
        licences_ids: Sequence[str] = []

        for _ in range(MAX_LICENCES):

            new_serial = await generate_new_serial_number()
            if new_serial == "":
                raise HTTPException(
                    status_code=500,
                    detail=HttpErrorsEnum.ERROR_WHILE_GENERATING_SERIAL_NUMBER.value,
                )

            licence_with_serial: Licences = await get_licence_from_serial_dal(
                db, new_serial
            )

            if licence_with_serial is not None:
                raise HTTPException(
                    status_code=500,
                    detail=HttpErrorsEnum.ERROR_WHILE_GENERATING_SERIAL_NUMBER.value,
                )

            licence: Licences = Licences(
                id=str(uuid4()),
                licence_type=None,
                serial_number=new_serial,
                demo_flag=infos.demo_flag,
            )
            licences.append(licence)
            licences_ids.append(licence.id)

        licence_index = 0
        # Create users
        for user in infos.users:

            if (
                infos.company_only
                and user.licence_type != TypeLicenceEnum.MICROPORT_STAFF.value
            ):
                raise HTTPException(
                    status_code=400,
                    detail=HttpErrorsEnum.USER_LICENCE_TYPE_ERROR.value,
                )

            if (
                not infos.company_only
                and user.licence_type == TypeLicenceEnum.MICROPORT_STAFF.value
            ):
                raise HTTPException(
                    status_code=400,
                    detail=HttpErrorsEnum.USER_LICENCE_TYPE_ERROR.value,
                )

            new_user = await get_user_from_keycloak_by_email(user.email)

            if len(new_user) == 0:
                # Create user in keycloak
                new_password = await generate_new_password()

                msg: MIMEMultipart = await build_email_new_user(user, new_password)

                await send_mail([user.email], msg)

                await post_user_with_licence_to_keycloak(
                    licences[licence_index].id,
                    user.firstname,
                    user.lastname,
                    user.email,
                    new_password,
                )

                new_user = await get_user_from_keycloak_by_email(user.email)

                await update_user_groups_from_keycloak(
                    new_user[0]["id"], user.licence_type
                )

                await put_user_to_keycloak(
                    new_user[0]["id"],
                    user.firstname,
                    user.lastname,
                    user.email,
                    licences[licence_index].id,
                    resetRequiredActions=True,
                    is_otp=False,  # user.type_2fa == Type2FA.MOBILE_APP.value,
                )

                licences[licence_index].id_user = new_user[0]["id"]
                licences[licence_index].licence_type = user.licence_type
                licence_index += 1

            else:
                if (
                    "attributes" in new_user[0]
                    and len(new_user[0]["attributes"]["licence_id"]) > 0
                ):
                    local_admin = await get_user_from_keycloak_by_id(
                        str(local_admin_id)
                    )

                    if local_admin.status_code == 200:
                        local_admin = local_admin.json()

                        msg: MIMEMultipart = (
                            await build_email_licence_already_used_local_admin(
                                user,
                                UsersDict(
                                    email=local_admin["email"],
                                    type_2fa=Type2FA.MOBILE_APP.value,
                                    licence_type=TypeLicenceEnum.HDS_LOCAL_ADMIN.value,
                                    firstname=local_admin["firstName"],
                                    lastname=local_admin["lastName"],
                                ),
                            )
                        )
                        await send_mail([user.email, infos.local_admin_email], msg)

                else:
                    await put_user_to_keycloak(
                        new_user[0]["id"],
                        user.firstname,
                        user.lastname,
                        user.email,
                        licences[licence_index].id,
                        user.type_2fa == Type2FA.MOBILE_APP.value,
                    )
                    new_user = await get_user_from_keycloak_by_email(user.email)

                    await update_user_groups_from_keycloak(
                        new_user[0]["id"], user.licence_type
                    )

                    licences[licence_index].id_user = new_user[0]["id"]
                    licences[licence_index].licence_type = user.licence_type
                    licence_index += 1

        licences[licence_index].id_user = local_admin_id
        licences[licence_index].licence_type = TypeLicenceEnum.NON_MEDICAL_STAFF.value

        # Create seller
        seller = await get_seller_by_email_dal(db, infos.seller_email)

        if seller is None:
            seller = Sellers(
                id=str(uuid4()),
                email=infos.seller_email,
                firstname=infos.seller_firstname,
                lastname=infos.seller_lastname,
                phone=infos.seller_phone,
            )
            await create_seller_dal(db, seller)

        created_at = actual_time_in_ms()

        # Create orders
        order = Orders(
            id=id_order,
            order_id=infos.order_id,
            seller_id=seller.id,
            local_admin_id=local_admin_id,
            state=StateOrderEnum.ACCEPTED.value,
            billing_type=infos.billing_type,
            country=infos.country,
            workplace=infos.workplace,
            service=infos.service,
            state_flag=StateOrderEnum.ACCEPTED.value,
            sending_date=created_at,
            order_accepted_date=created_at,
            demo_flag=infos.demo_flag,
            sharing_authorization=infos.sharing_authorization,
            company_only=infos.company_only,
        )

        await create_order_dal(db, order)

        for licence in licences:
            licence.id_order = id_order
            await create_licence_dal(db, licence)

        local_admin_licence.id_order = id_order
        await create_licence_dal(db, local_admin_licence)

        await sio.emit("orders", room=payload["sub"])

        return order

    raise HTTPException(status_code=403)

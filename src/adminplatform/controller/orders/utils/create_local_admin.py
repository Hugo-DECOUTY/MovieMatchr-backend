from uuid import uuid4
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException
from re import sub
from sqlalchemy.ext.asyncio import AsyncSession

from adminplatform.enum.errors.HttpErrorsEnum import HttpErrorsEnum

from adminplatform.schemas.orders.info_post_orders import InfoPostOrders
from adminplatform.schemas.licences.licences import Licences
from adminplatform.schemas.licences.licences import TypeLicenceEnum

from adminplatform.services.licences import get_licence_from_serial_dal
from adminplatform.services.orders import get_orders_from_local_admin_dal

from adminplatform.services.keycloak.post.post_local_admin_to_keycloak import (
    post_local_admin_to_keycloak,
)
from adminplatform.services.keycloak.get.get_user_from_keycloak_by_email import (
    get_user_from_keycloak_by_email,
)
from adminplatform.services.keycloak.update.update_user_groups_from_keycloak import (
    update_user_groups_from_keycloak,
)
from adminplatform.services.keycloak.put.put_user_to_keycloak import (
    put_user_to_keycloak,
)

from adminplatform.utils.generate_new_serial_number import generate_new_serial_number
from adminplatform.utils.generate_new_password import generate_new_password
from adminplatform.utils.mail.build_email_new_local_admin import (
    build_email_new_local_admin,
)

from adminplatform.utils.mail.send_mail import send_mail


def snake_case(string: str) -> str:
    return "".join(
        sub(
            "([A-Z][a-z]+)", r" \1", sub("([A-Z]+)", r" \1", string.replace("-", " "))
        ).split()
    ).lower()


def clear_unvalid_char(string: str) -> str:
    not_allowed_chars = [
        "!",
        "#",
        "$",
        "%",
        "&",
        "'",
        "*",
        "+",
        "/",
        "=",
        "?",
        "^",
        "`",
        "{",
        "|",
        "}",
        "~",
        '"',
        "(",
        ")",
        ",",
        ":",
        ";",
        "<",
        ">",
        "[",
        "]",
        "\\",
        " ",
    ]
    cleaned_email = ""
    for char in string:
        if char not in not_allowed_chars:
            cleaned_email += char
    return cleaned_email


async def create_local_admin(db: AsyncSession, infos: InfoPostOrders):
    local_admin = await get_user_from_keycloak_by_email(infos.local_admin_email)

    orders_local_admin = []

    if len(local_admin) == 0:
        new_password = await generate_new_password()

        msg: MIMEMultipart = await build_email_new_local_admin(
            {
                "email": infos.local_admin_email,
                "firstname": infos.local_admin_firstname,
                "lastname": infos.local_admin_lastname,
            },
            new_password,
        )

        await send_mail([infos.local_admin_email], msg)

        await post_local_admin_to_keycloak(
            infos.local_admin_email,
            infos.local_admin_firstname,
            infos.local_admin_lastname,
            new_password,
        )

        local_admin_id = (
            await get_user_from_keycloak_by_email(infos.local_admin_email)
        )[0]["id"]
    else:
        orders_local_admin = await get_orders_from_local_admin_dal(
            db, local_admin[0]["id"]
        )
        if len(orders_local_admin) == 0:
            local_admin_id = local_admin[0]["id"]
        else:
            # Generate admin with tag in email
            new_password = await generate_new_password()
            domain = infos.local_admin_email.split("@")[-1]
            name_email = infos.local_admin_email.split("@")[0]
            if len(infos.workplace) and len(infos.service):
                email_tag: str = f"{name_email}+{clear_unvalid_char(snake_case(infos.workplace))}.{clear_unvalid_char(snake_case(infos.service))}@{domain}"
            else:
                email_tag: str = f"{name_email}+{str(uuid4())[:8]}@{domain}"
            msg: MIMEMultipart = await build_email_new_local_admin(
                {
                    "email": email_tag,
                    "firstname": infos.local_admin_firstname,
                    "lastname": infos.local_admin_lastname,
                },
                new_password,
            )

            await send_mail([email_tag], msg)

            await post_local_admin_to_keycloak(
                email_tag,
                infos.local_admin_firstname,
                infos.local_admin_lastname,
                new_password,
            )

            local_admin_id = (await get_user_from_keycloak_by_email(email_tag))[0]["id"]

    await update_user_groups_from_keycloak(
        local_admin_id, TypeLicenceEnum.HDS_LOCAL_ADMIN.value
    )

    new_serial = await generate_new_serial_number()
    if new_serial == "":
        raise HTTPException(
            status_code=500,
            detail=HttpErrorsEnum.ERROR_WHILE_GENERATING_SERIAL_NUMBER.value,
        )

    licence_with_serial: Licences = await get_licence_from_serial_dal(db, new_serial)

    if licence_with_serial is not None:
        raise HTTPException(
            status_code=500,
            detail=HttpErrorsEnum.ERROR_WHILE_GENERATING_SERIAL_NUMBER.value,
        )

    local_admin_licence: Licences = Licences(
        id=str(uuid4()),
        licence_type=TypeLicenceEnum.NON_MEDICAL_STAFF.value,
        serial_number=new_serial,
        demo_flag=infos.demo_flag,
        id_user=local_admin_id,
    )

    await update_user_groups_from_keycloak(
        local_admin_id, TypeLicenceEnum.NON_MEDICAL_STAFF.value
    )

    if len(orders_local_admin) == 0:
        await put_user_to_keycloak(
            local_admin_id,
            infos.local_admin_firstname,
            infos.local_admin_lastname,
            infos.local_admin_email,
            local_admin_licence.id,
        )
    else:
        await put_user_to_keycloak(
            local_admin_id,
            infos.local_admin_firstname,
            infos.local_admin_lastname,
            email_tag,
            local_admin_licence.id,
            linked_account=local_admin[0]["id"],
        )

    return local_admin_licence, local_admin_id

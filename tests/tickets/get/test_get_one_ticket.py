import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from adminplatform.schemas.tickets.tickets import TypeTicketEnum, StateTicketEnum
from adminplatform.schemas.account.user import Type2FA

from adminplatform.enum.errors.HttpErrorsEnum import HttpErrorsEnum

from tests.conftest import (
    ACCESS_TOKEN_ADMIN,
    ACCESS_TOKEN_LOCAL_ADMIN,
    ACCESS_TOKEN_UNKNOWN_USER,
    UUID_ADMIN,
    UUID_LOCAL_ADMIN,
    UUID_ORDER_1,
    UUID_TICKET_NOT_FOUND,
    UUID_TICKET_1,
    UUID_TICKET_2,
    UUID_TICKET_3,
    UUID_TICKET_4,
    pre_fill_db,
)

@pytest.mark.asyncio
async def test_get_one_ticket_from_admin(client: AsyncClient, session: AsyncSession) -> None:
    await pre_fill_db(session)
    response = await client.get(
            f"/tickets/{UUID_TICKET_NOT_FOUND}",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN}
        )
    assert response.status_code == 404
    assert response.json() == {"detail": HttpErrorsEnum.TICKET_NOT_FOUND.value}

    response = await client.get(
            f"/tickets/{UUID_TICKET_1}",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == {
            "id": UUID_TICKET_1,
            "id_order": UUID_ORDER_1,
            "user": UUID_LOCAL_ADMIN,
            "type": TypeTicketEnum.MODIFY_USER.value,
            "sending_date": 1666870958,
            "body": {
                "id": None,
                "type_2fa": Type2FA.EMAIL.value,
                "email": "sjeanpro28@gmail.com",
                "new_email": "sjeanpro28@gmail.com",
                "firstname": "Samuel_Test",
                "lastname": "Jean_Test",
                "serial_number": None,
                "licence_type": None,
            },
            "state_flag": StateTicketEnum.IN_PROGRESS.value,
            "update_state_date": None,
        }

    response = await client.get(
            f"/tickets/{UUID_TICKET_2}",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == {
            "id": UUID_TICKET_2,
            "id_order": UUID_ORDER_1,
            "user": UUID_ADMIN,
            "type": TypeTicketEnum.MODIFY_USER.value,
            "sending_date": 1666870958,
            "body": {
                "id": None,
                "type_2fa": Type2FA.EMAIL.value,
                "email": "sjeanpro28@gmail.com",
                "new_email": "sjeanpro28@gmail.com",
                "firstname": "Samuel_Test",
                "lastname": "Jean_Test",
                "serial_number": None,
                "licence_type": None,
            },
            "state_flag": StateTicketEnum.IN_PROGRESS.value,
            "update_state_date": None,
        }

    response = await client.get(
            f"/tickets/{UUID_TICKET_3}",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == {
            "id": UUID_TICKET_3,
            "id_order": UUID_ORDER_1,
            "user": UUID_LOCAL_ADMIN,
            "type": TypeTicketEnum.MODIFY_USER.value,
            "sending_date": 1666870958,
            "body": {
                "id": None,
                "type_2fa": Type2FA.EMAIL.value,
                "email": "sjeanpro28@gmail.com",
                "new_email": "sjeanpro28@gmail.com",
                "firstname": "Samuel_Test",
                "lastname": "Jean_Test",
                "serial_number": None,
                "licence_type": None,
            },
            "state_flag": StateTicketEnum.IN_PROGRESS.value,
            "update_state_date": None,
        }

    response = await client.get(
            f"/tickets/{UUID_TICKET_4}",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == {
            "id": UUID_TICKET_4,
            "id_order": UUID_ORDER_1,
            "user": UUID_ADMIN,
            "type": TypeTicketEnum.MODIFY_USER.value,
            "sending_date": 1666870958,
            "body": {
                "id": None,
                "type_2fa": Type2FA.EMAIL.value,
                "email": "sjeanpro28@gmail.com",
                "new_email": "sjeanpro28@gmail.com",
                "firstname": "Samuel_Test",
                "lastname": "Jean_Test",
                "serial_number": None,
                "licence_type": None,
            },
            "state_flag": StateTicketEnum.IN_PROGRESS.value,
            "update_state_date": None,
        }

@pytest.mark.asyncio
async def test_get_one_ticket_from_local_admin(client: AsyncClient, session: AsyncSession) -> None:
    await pre_fill_db(session)
    response = await client.get(
            f"/tickets/{UUID_TICKET_NOT_FOUND}",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN}
        )
    assert response.status_code == 404
    assert response.json() == {"detail": HttpErrorsEnum.TICKET_NOT_FOUND.value}

    response = await client.get(
            f"/tickets/{UUID_TICKET_1}",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == {
            "id": UUID_TICKET_1,
            "id_order": UUID_ORDER_1,
            "user": UUID_LOCAL_ADMIN,
            "type": TypeTicketEnum.MODIFY_USER.value,
            "sending_date": 1666870958,
            "body": {
                "id": None,
                "type_2fa": Type2FA.EMAIL.value,
                "email": "sjeanpro28@gmail.com",
                "new_email": "sjeanpro28@gmail.com",
                "firstname": "Samuel_Test",
                "lastname": "Jean_Test",
                "serial_number": None,
                "licence_type": None,
            },
            "state_flag": StateTicketEnum.IN_PROGRESS.value,
            "update_state_date": None,
        }

    response = await client.get(
            f"/tickets/{UUID_TICKET_3}",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == {
            "id": UUID_TICKET_3,
            "id_order": UUID_ORDER_1,
            "user": UUID_LOCAL_ADMIN,
            "type": TypeTicketEnum.MODIFY_USER.value,
            "sending_date": 1666870958,
            "body": {
                "id": None,
                "type_2fa": Type2FA.EMAIL.value,
                "email": "sjeanpro28@gmail.com",
                "new_email": "sjeanpro28@gmail.com",
                "firstname": "Samuel_Test",
                "lastname": "Jean_Test",
                "serial_number": None,
                "licence_type": None,
            },
            "state_flag": StateTicketEnum.IN_PROGRESS.value,
            "update_state_date": None,
        }

@pytest.mark.asyncio
async def test_get_one_ticket_from_local_admin_forbidden(client: AsyncClient, session: AsyncSession) -> None:
    await pre_fill_db(session)
    response = await client.get(
            f"/tickets/{UUID_TICKET_2}",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": HttpErrorsEnum.YOU_DO_NOT_OWN_THIS_TICKET.value}

    response = await client.get(
            f"/tickets/{UUID_TICKET_4}",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": HttpErrorsEnum.YOU_DO_NOT_OWN_THIS_TICKET.value}

@pytest.mark.asyncio
async def test_get_one_ticket_from_unknown_user_forbidden(client: AsyncClient, session: AsyncSession) -> None:
    await pre_fill_db(session)
    response = await client.get(
            f"/tickets/{UUID_TICKET_NOT_FOUND}",
            headers={"X-USERINFO": ACCESS_TOKEN_UNKNOWN_USER}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.get(
            f"/tickets/{UUID_TICKET_1}",
            headers={"X-USERINFO": ACCESS_TOKEN_UNKNOWN_USER}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.get(
            f"/tickets/{UUID_TICKET_2}",
            headers={"X-USERINFO": ACCESS_TOKEN_UNKNOWN_USER}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.get(
            f"/tickets/{UUID_TICKET_3}",
            headers={"X-USERINFO": ACCESS_TOKEN_UNKNOWN_USER}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.get(
            f"/tickets/{UUID_TICKET_4}",
            headers={"X-USERINFO": ACCESS_TOKEN_UNKNOWN_USER}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

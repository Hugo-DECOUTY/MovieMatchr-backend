from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv
import pytest

from adminplatform.schemas.licences.licences import TypeLicenceEnum
from adminplatform.schemas.tickets.tickets import TypeTicketEnum

from adminplatform.schemas.account.user import Type2FA

from adminplatform.enum.errors.HttpErrorsEnum import HttpErrorsEnum

from tests.conftest import (
    ACCESS_TOKEN_ADMIN,
    ACCESS_TOKEN_LOCAL_ADMIN,
    ACCESS_TOKEN_UNKNOWN_USER,
    UUID_ORDER_NOT_FOUND,
    UUID_ORDER_1,
    UUID_ORDER_2,
    UUID_ORDER_3,
    UUID_ORDER_4,
    pre_fill_db,
)

load_dotenv()

@pytest.mark.asyncio
async def test_post_ticket_from_admin(client: AsyncClient, session: AsyncSession) -> None:
    await pre_fill_db(session)
    response = await client.get(
            "/tickets",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN},
        )
    assert response.status_code == 200
    assert len(response.json()) == 4

    response = await client.post(
        "/tickets",
        headers={"X-USERINFO": ACCESS_TOKEN_ADMIN},
        json={
            "id_order": UUID_ORDER_1,
            "type": TypeTicketEnum.MODIFY_USER.value,
            "body": {
                "type_2fa": Type2FA.EMAIL.value,
                "email": "sjeanpro28@gmail.com",
                "new_email": "sjeanpro28@gmail.com",
                "firstname": "Samuel_Test",
                "lastname": "Jean_Test",
            },
        },
    )
    assert response.status_code == 201

    response = await client.get(
            "/tickets",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN},
        )    
    assert response.status_code == 200
    assert len(response.json()) == 5

    response = await client.post(
        "/tickets",
        headers={"X-USERINFO": ACCESS_TOKEN_ADMIN},
        json={
            "id_order": UUID_ORDER_2,
            "type": TypeTicketEnum.MODIFY_USER.value,
            "body": {
                "type_2fa": Type2FA.EMAIL.value,
                "email": "sjeanpro28@gmail.com",
                "new_email": "sjeanpro28@gmail.com",
                "firstname": "Samuel_Test",
                "lastname": "Jean_Test",
            },
        },
    )
    assert response.status_code == 201

    response = await client.get(
            "/tickets",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN},
        )    
    assert response.status_code == 200
    assert len(response.json()) == 6

    response = await client.post(
        "/tickets",
        headers={"X-USERINFO": ACCESS_TOKEN_ADMIN},
        json={
            "id_order": UUID_ORDER_3,
            "type": TypeTicketEnum.MODIFY_USER.value,
            "body": {
                "type_2fa": Type2FA.EMAIL.value,
                "email": "sjeanpro28@gmail.com",
                "new_email": "sjeanpro28@gmail.com",
                "firstname": "Samuel_Test",
                "lastname": "Jean_Test",
            },
        },
    )
    assert response.status_code == 201

    response = await client.get(
            "/tickets",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN},
        )    
    assert response.status_code == 200
    assert len(response.json()) == 7

    response = await client.post(
        "/tickets",
        headers={"X-USERINFO": ACCESS_TOKEN_ADMIN},
        json={
            "id_order": UUID_ORDER_NOT_FOUND,
            "type": TypeTicketEnum.ADD_NEW_LICENCES.value,
            "body": {
                "firstname": "DOC1Firstname",
                "lastname": "DOC1Lastname",
                "email": "doc1@test.com",
                "licence_type": TypeLicenceEnum.DOCTOR.value,
            }
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": HttpErrorsEnum.ORDER_NOT_FOUND.value}

    response = await client.get(
            "/tickets",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN},
        )    
    assert response.status_code == 200
    assert len(response.json()) == 7

    response = await client.post(
        "/tickets",
        headers={"X-USERINFO": ACCESS_TOKEN_ADMIN},
        json={
            "id_order": UUID_ORDER_4,
            "type": TypeTicketEnum.MODIFY_USER.value,
            "body": {
                "type_2fa": Type2FA.EMAIL.value,
                "email": "test_unknown@gmail.com",
                "new_email": "test_unknown@gmail.com",
                "firstname": "Samuel_Test",
                "lastname": "Jean_Test",
            },
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": HttpErrorsEnum.USER_NOT_FOUND.value}

    response = await client.get(
            "/tickets",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN},
        )    
    assert response.status_code == 200
    assert len(response.json()) == 7

@pytest.mark.asyncio
async def test_post_ticket_from_local_admin(client: AsyncClient, session: AsyncSession) -> None:
    await pre_fill_db(session)
    response = await client.get(
            "/tickets",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN},
        )
    assert response.status_code == 200
    assert len(response.json()) == 2

    response = await client.post(
        "/tickets",
        headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN},
        json={
            "id_order": UUID_ORDER_1,
            "type": TypeTicketEnum.MODIFY_USER.value,
            "body": {
                "type_2fa": Type2FA.EMAIL.value,
                "email": "sjeanpro28@gmail.com",
                "new_email": "sjeanpro28@gmail.com",
                "firstname": "Samuel_Test",
                "lastname": "Jean_Test",
            },
        },
    )
    assert response.status_code == 201

    response = await client.get(
            "/tickets",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN},
        )    
    assert response.status_code == 200
    assert len(response.json()) == 3

    response = await client.post(
        "/tickets",
        headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN},
        json={
            "id_order": UUID_ORDER_3,
            "type": TypeTicketEnum.MODIFY_USER.value,
            "body": {
                "type_2fa": Type2FA.EMAIL.value,
                "email": "sjeanpro28@gmail.com",
                "new_email": "sjeanpro28@gmail.com",
                "firstname": "Samuel_Test",
                "lastname": "Jean_Test",
            },
        },
    )
    assert response.status_code == 403
    assert response.json() == {"detail": HttpErrorsEnum.YOU_DO_NOT_OWN_THIS_ORDER.value}

    response = await client.get(
            "/tickets",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN},
        )    
    assert response.status_code == 200
    assert len(response.json()) == 3

    response = await client.post(
        "/tickets",
        headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN},
        json={
            "id_order": UUID_ORDER_1,
            "type": TypeTicketEnum.MODIFY_USER.value,
            "body": {
                "type_2fa": Type2FA.EMAIL.value,
                "email": "sjeanpro28@gmail.com",
                "new_email": "sjeanpro28@gmail.com",
                "firstname": "Samuel_Test",
                "lastname": "Jean_Test",
            },
        },
    )
    assert response.status_code == 201

    response = await client.get(
            "/tickets",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN},
        )    
    assert response.status_code == 200
    assert len(response.json()) == 4

    response = await client.post(
        "/tickets",
        headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN},
        json={
            "id_order": UUID_ORDER_NOT_FOUND,
            "type": TypeTicketEnum.ADD_NEW_LICENCES.value,
            "body": {
                "firstname": "DOC1Firstname",
                "lastname": "DOC1Lastname",
                "email": "doc1@test.com",
                "licence_type": TypeLicenceEnum.DOCTOR.value,
            }
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": HttpErrorsEnum.ORDER_NOT_FOUND.value}

    response = await client.get(
            "/tickets",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN},
        )    
    assert response.status_code == 200
    assert len(response.json()) == 4

    response = await client.post(
        "/tickets",
        headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN},
        json={
            "id_order": UUID_ORDER_1,
            "type": TypeTicketEnum.MODIFY_USER.value,
            "body": {
                "firstname": "TestTicket1",
                "lastname": "Test",
                "email": "test_adminplatform_doctor1_error@test.com",
                "new_email": "test_adminplatform_doctor1@test.com",
            }
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": HttpErrorsEnum.USER_NOT_FOUND.value}

    response = await client.get(
            "/tickets",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN},
        )    
    assert response.status_code == 200
    assert len(response.json()) == 4

@pytest.mark.asyncio
async def test_post_ticket_from_unknown_user_forbidden(client: AsyncClient, session: AsyncSession) -> None:
    await pre_fill_db(session)
    response = await client.post(
        "/tickets",
        headers={"X-USERINFO": ACCESS_TOKEN_UNKNOWN_USER},
        json={
            "id_order": UUID_ORDER_NOT_FOUND,
            "type": TypeTicketEnum.MODIFY_USER.value,
            "body": {
                "firstname": "TestTicket1",
                "lastname": "Test",
                "email": "test_adminplatform_doctor1@test.com",
                "new_email": "test_adminplatform_doctor1@test.com",
            }
        },
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.post(
        "/tickets",
        headers={"X-USERINFO": ACCESS_TOKEN_UNKNOWN_USER},
        json={
            "id_order": UUID_ORDER_1,
            "type": TypeTicketEnum.MODIFY_USER.value,
            "body": {
                "firstname": "TestTicket1",
                "lastname": "Test",
                "email": "test_adminplatform_doctor1@test.com",
                "new_email": "test_adminplatform_doctor1@test.com",
            }
        },
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.post(
        "/tickets",
        headers={"X-USERINFO": ACCESS_TOKEN_UNKNOWN_USER},
        json={
            "id_order": UUID_ORDER_3,
            "type": TypeTicketEnum.ADD_NON_MEDICAL_PERSONEL.value,
            "body": {
                "firstname": "TestTicket2",
                "lastname": "Test",
                "email": "test_ticket2@test.com",
            }
        },
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}
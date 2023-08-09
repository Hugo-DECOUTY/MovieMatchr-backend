import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from adminplatform.schemas.tickets.tickets import TypeTicketEnum, StateTicketEnum
from adminplatform.schemas.licences.licences import TypeLicenceEnum
from adminplatform.schemas.account.user import Type2FA

from adminplatform.enum.errors.HttpErrorsEnum import HttpErrorsEnum

from tests.conftest import (
    ACCESS_TOKEN_ADMIN,
    ACCESS_TOKEN_LOCAL_ADMIN,
    UUID_TICKET_NOT_FOUND,
    UUID_TICKET_1,
    UUID_TICKET_2,
    UUID_TICKET_3,
    UUID_TICKET_4,
    pre_fill_db,
)

@pytest.mark.asyncio
async def test_patch_one_ticket_from_admin(client: AsyncClient, session: AsyncSession) -> None:
    await pre_fill_db(session)
    response = await client.patch(
            f"/tickets/{UUID_TICKET_NOT_FOUND}",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN},
            json={
                "type": TypeTicketEnum.MODIFY_USER.value,
                "body": {
                    "id": None,
                    "email": "sjeanpro28@gmail.com",
                    "new_email": "sjeanpro28_patch@gmail.com",
                    "firstname": "Samuel_Test_Patch",
                    "lastname": "Jean_Test_Patch",
                    "licence_type": None,
                },
                "state_flag": StateTicketEnum.ACCEPTED.value,
            }
        )
    assert response.status_code == 404
    assert response.json() == {"detail": HttpErrorsEnum.TICKET_NOT_FOUND.value}

    response = await client.patch(
            f"/tickets/{UUID_TICKET_1}",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN},
            json={
                "type": TypeTicketEnum.MODIFY_USER.value,
                "body": {
                    "id": None,
                    "type_2fa": Type2FA.EMAIL.value,
                    "email": "sjeanpro28@gmail.com",
                    "new_email": "sjeanpro28_patch@gmail.com",
                    "firstname": "Samuel_Test_Patch",
                    "lastname": "Jean_Test_Patch",
                    "serial_number": None,
                    "licence_type": None,
                },
                "state_flag": StateTicketEnum.ACCEPTED.value,
            }
        )
    
    assert response.status_code == 204
    assert response.json()["type"] == TypeTicketEnum.MODIFY_USER.value
    assert response.json()["body"] == {
                    "id": None,
                    "type_2fa": Type2FA.EMAIL.value,
                    "email": "sjeanpro28@gmail.com",
                    "new_email": "sjeanpro28_patch@gmail.com",
                    "firstname": "Samuel_Test_Patch",
                    "lastname": "Jean_Test_Patch",
                    "serial_number": None,
                    "licence_type": None,
                }
    assert response.json()["state_flag"] == StateTicketEnum.ACCEPTED.value

    response = await client.patch(
            f"/tickets/{UUID_TICKET_2}",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN},
            json={
                "type": TypeTicketEnum.MODIFY_USER.value,
                "body": {
                    "id": None,
                    "type_2fa": Type2FA.MOBILE_APP.value,
                    "email": "sjeanpro28@gmail.com",
                    "new_email": "sjeanpro28_patch2@gmail.com",
                    "firstname": "Samuel_Test_Patch2",
                    "lastname": "Jean_Test_Patch2",
                    "serial_number": None,
                    "licence_type": None,
                },
                "state_flag": StateTicketEnum.DENIED.value,
            }
        )
    
    assert response.status_code == 204
    assert response.json()["type"] == TypeTicketEnum.MODIFY_USER.value
    assert response.json()["body"] == {
                    "id": None,
                    "type_2fa": Type2FA.MOBILE_APP.value,
                    "email": "sjeanpro28@gmail.com",
                    "new_email": "sjeanpro28_patch2@gmail.com",
                    "firstname": "Samuel_Test_Patch2",
                    "lastname": "Jean_Test_Patch2",
                    "serial_number": None,
                    "licence_type": None,
    }
    assert response.json()["state_flag"] == StateTicketEnum.DENIED.value

    response = await client.patch(
            f"/tickets/{UUID_TICKET_2}",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN},
            json={
                "type": TypeTicketEnum.MODIFY_USER.value,
                "body": {
                    "id": None,
                    "type_2fa": Type2FA.EMAIL.value,
                    "email": "sjeanpro28@gmail.com",
                    "new_email": "sjeanpro28_patch2@gmail.com",
                    "firstname": "Samuel_Test_Patch2",
                    "lastname": "Jean_Test_Patch2",
                    "serial_number": None,
                    "licence_type": None,
                },
                "state_flag": StateTicketEnum.CANCELED.value,
            }
        )
    
    assert response.status_code == 204
    assert response.json()["type"] == TypeTicketEnum.MODIFY_USER.value
    assert response.json()["body"] == {
                    "id": None,
                    "type_2fa": Type2FA.EMAIL.value,
                    "email": "sjeanpro28@gmail.com",
                    "new_email": "sjeanpro28_patch2@gmail.com",
                    "firstname": "Samuel_Test_Patch2",
                    "lastname": "Jean_Test_Patch2",
                    "serial_number": None,
                    "licence_type": None,
                }
    assert response.json()["state_flag"] == StateTicketEnum.CANCELED.value

    response = await client.patch(
            f"/tickets/{UUID_TICKET_2}",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN},
            json={
                "type": TypeTicketEnum.MODIFY_USER.value,
                "body": {
                    "id": None,
                    "type_2fa": Type2FA.MOBILE_APP.value,
                    "email": "sjeanpro28@gmail.com",
                    "new_email": "sjeanpro28_patch2@gmail.com",
                    "firstname": "Samuel_Test_Patch2",
                    "lastname": "Jean_Test_Patch2",
                    "serial_number": None,
                    "licence_type": None,
                },
            }
        )
    
    assert response.status_code == 422

    response = await client.patch(
            f"/tickets/{UUID_TICKET_2}",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN},
            json={
                "body": {
                    "id": None,
                    "email": "nmp1_patch@gmail.com",
                    "new_email": None,
                    "firstname": "NMPFirstname_patch",
                    "lastname": "NMPLastname_patch",
                    "licence_type": None,
                },
                "state_flag": StateTicketEnum.ACCEPTED.value,
            }
        )
    
    assert response.status_code == 422

    response = await client.patch(
            f"/tickets/{UUID_TICKET_2}",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN},
            json={
                "type": TypeTicketEnum.MODIFY_USER.value,
                "state_flag": StateTicketEnum.ACCEPTED.value,
            }
        )
    
    assert response.status_code == 422

    response = await client.patch(
            f"/tickets/{UUID_TICKET_4}",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN},
            json={
                "type": TypeTicketEnum.MODIFY_USER.value,
                "body": {
                    "id": None,
                    "type_2fa": Type2FA.MOBILE_APP.value,
                    "email": "sjeanpro28@gmail.com",
                    "new_email": "sjeanpro28_patch2@gmail.com",
                    "firstname": "Samuel_Test_Patch2",
                    "lastname": "Jean_Test_Patch2",
                    "serial_number": None,
                    "licence_type": None,
                },
                "state_flag": StateTicketEnum.IN_PROGRESS.value,
            }
        )
    
    assert response.status_code == 204
    assert response.json()["type"] == TypeTicketEnum.MODIFY_USER.value
    assert response.json()["body"] == {
                    "id": None,
                    "type_2fa": Type2FA.MOBILE_APP.value,
                    "email": "sjeanpro28@gmail.com",
                    "new_email": "sjeanpro28_patch2@gmail.com",
                    "firstname": "Samuel_Test_Patch2",
                    "lastname": "Jean_Test_Patch2",
                    "serial_number": None,
                    "licence_type": None,
                }
    assert response.json()["state_flag"] == StateTicketEnum.IN_PROGRESS.value

@pytest.mark.asyncio
async def test_patch_one_ticket_from_local_admin(client: AsyncClient, session: AsyncSession) -> None:
    await pre_fill_db(session)
    response = await client.patch(
            f"/tickets/{UUID_TICKET_NOT_FOUND}",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN},
            json={
                "type": TypeTicketEnum.ADD_NON_MEDICAL_PERSONEL.value,
                "body": {
                    "firstname": "TestTicketNotFound",
                    "lastname": "Test",
                    "email": "test_ticket_not_found@test.com",
                },
                "state_flag": StateTicketEnum.IN_PROGRESS.value,
            }
        )
    assert response.status_code == 404
    assert response.json() == {"detail": HttpErrorsEnum.TICKET_NOT_FOUND.value}

    response = await client.patch(
            f"/tickets/{UUID_TICKET_1}",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN},
            json={
                "type": TypeTicketEnum.MODIFY_USER.value,
                "body": {
                    "id": None,
                    "type_2fa": Type2FA.EMAIL.value,
                    "email": "sjeanpro28@gmail.com",
                    "new_email": "sjeanpro28_patch@gmail.com",
                    "firstname": "Samuel_Test_Patch",
                    "lastname": "Jean_Test_Patch",
                    "serial_number": None,
                    "licence_type": None,
                },
                "state_flag": StateTicketEnum.ACCEPTED.value,
            }
        )
    
    assert response.status_code == 403

    response = await client.patch(
            f"/tickets/{UUID_TICKET_2}",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN},
            json={
                "type": TypeTicketEnum.MODIFY_USER.value,
                "body": {
                    "id": None,
                    "type_2fa": Type2FA.MOBILE_APP.value,
                    "email": "sjeanpro28@gmail.com",
                    "new_email": "sjeanpro28_patch2@gmail.com",
                    "firstname": "Samuel_Test_Patch2",
                    "lastname": "Jean_Test_Patch2",
                    "serial_number": None,
                    "licence_type": None,
                },
                "state_flag": StateTicketEnum.DENIED.value,
            }
        )
    
    assert response.status_code == 403
    assert response.json() == {"detail": HttpErrorsEnum.YOU_DO_NOT_OWN_THIS_TICKET.value}

    response = await client.patch(
            f"/tickets/{UUID_TICKET_2}",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN},
            json={
                "type": TypeTicketEnum.MODIFY_USER.value,
                "body": {
                    "id": None,
                    "type_2fa": Type2FA.MOBILE_APP.value,
                    "email": "sjeanpro28@gmail.com",
                    "new_email": "sjeanpro28_patch2@gmail.com",
                    "firstname": "Samuel_Test_Patch2",
                    "lastname": "Jean_Test_Patch2",
                    "serial_number": None,
                    "licence_type": None,
                },
                "state_flag": StateTicketEnum.DENIED.value,
            }
        )
    
    assert response.status_code == 403
    assert response.json() == {"detail": HttpErrorsEnum.YOU_DO_NOT_OWN_THIS_TICKET.value}

    response = await client.patch(
            f"/tickets/{UUID_TICKET_2}",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN},
            json={
                "type": TypeTicketEnum.MODIFY_USER.value,
                "body": {
                    "id": None,
                    "type_2fa": Type2FA.EMAIL.value,
                    "email": "sjeanpro28@gmail.com",
                    "new_email": "sjeanpro28_patch2@gmail.com",
                    "firstname": "Samuel_Test_Patch2",
                    "lastname": "Jean_Test_Patch2",
                    "serial_number": None,
                    "licence_type": None,
                },
            }
        )
    
    assert response.status_code == 422

    response = await client.patch(
            f"/tickets/{UUID_TICKET_2}",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN},
            json={
                "body": {
                    "id": None,
                    "email": "nmp1_patch@gmail.com",
                    "new_email": None,
                    "firstname": "NMPFirstname_patch",
                    "lastname": "NMPLastname_patch",
                    "licence_type": None,
                },
                "state_flag": StateTicketEnum.ACCEPTED.value,
            }
        )
    
    assert response.status_code == 422

    response = await client.patch(
            f"/tickets/{UUID_TICKET_2}",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN},
            json={
                "type": TypeTicketEnum.ADD_NON_MEDICAL_PERSONEL.value,
                "state_flag": StateTicketEnum.ACCEPTED.value,
            }
        )
    
    assert response.status_code == 422

    response = await client.patch(
            f"/tickets/{UUID_TICKET_3}",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN},
            json={
                "type": TypeTicketEnum.MODIFY_USER.value,
                "body": {
                    "id": None,
                    "type_2fa": Type2FA.EMAIL.value,
                    "email": "sjeanpro28@gmail.com",
                    "new_email": "sjeanpro28_patch2@gmail.com",
                    "firstname": "Samuel_Test_Patch2",
                    "lastname": "Jean_Test_Patch2",
                    "serial_number": None,
                    "licence_type": None,
                },
                "state_flag": StateTicketEnum.CANCELED.value,
            }
        )
    
    assert response.status_code == 204
    assert response.json()["type"] == TypeTicketEnum.MODIFY_USER.value
    assert response.json()["body"] == {
                    "id": None,
                    "type_2fa": Type2FA.EMAIL.value,
                    "email": "sjeanpro28@gmail.com",
                    "new_email": "sjeanpro28_patch2@gmail.com",
                    "firstname": "Samuel_Test_Patch2",
                    "lastname": "Jean_Test_Patch2",
                    "serial_number": None,
                    "licence_type": None,
                }
    assert response.json()["state_flag"] == StateTicketEnum.CANCELED.value

    response = await client.patch(
            f"/tickets/{UUID_TICKET_3}",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN},
            json={
                "type": TypeTicketEnum.ADD_NEW_LICENCES.value,
                "body": {
                    "id": None,
                    "email": "doc1_patch@gmail.com",
                    "new_email": None,
                    "firstname": "DOC1Firstname_patch",
                    "lastname": "DOC1Lastname_patch",
                    "licence_type": TypeLicenceEnum.DOCTOR.value,
                },
                "state_flag": StateTicketEnum.ACCEPTED.value,
            }
        )
    
    assert response.status_code == 403
    assert response.json() == {"detail": HttpErrorsEnum.TICKET_ALREADY_CLOSED.value}
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from adminplatform.schemas.licences.licences import TypeLicenceEnum
from adminplatform.schemas.account.user import Type2FA


from tests.conftest import (
    ACCESS_TOKEN_ADMIN,
    ACCESS_TOKEN_LOCAL_ADMIN,
    UUID_ORDER_1,
    UUID_ORDER_2,
    UUID_ORDER_3,
    UUID_ORDER_4,
    pre_fill_db,
)


@pytest.mark.asyncio
async def test_get_order_users_from_admin(client: AsyncClient, session: AsyncSession) -> None:
    await pre_fill_db(session)
    response = await client.get(
            f"/orders/{UUID_ORDER_1}/users",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == [
        {
            "type_2fa": Type2FA.EMAIL.value,
            "licence_type": TypeLicenceEnum.DOCTOR.value,
            "email": "test_adminplatform_doctor1@test.com",
            "firstname": "test_adminplatform_doctor1_firstname",
            "lastname": "test_adminplatform_doctor1_lastname",
        },
        {
            "type_2fa": Type2FA.EMAIL.value,
            "licence_type": TypeLicenceEnum.DOCTOR.value,
            "email": "test_adminplatform_doctor2@test.com",
            "firstname": "test_adminplatform_doctor2_firstname",
            "lastname": "test_adminplatform_doctor2_lastname",
        },
        {
            "type_2fa": Type2FA.EMAIL.value,
            "licence_type": TypeLicenceEnum.MEDICAL_STAFF.value,
            "email": "test_adminplatform_medicalstaff1@test.com",
            "firstname": "test_adminplatform_medicalstaff1_firstname",
            "lastname": "test_adminplatform_medicalstaff1_lastname",
        },
    ]

    response = await client.get(
            f"/orders/{UUID_ORDER_2}/users",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == [
        {
            "type_2fa": Type2FA.EMAIL.value,
            "licence_type": TypeLicenceEnum.DOCTOR.value,
            "email": "test_adminplatform_doctor3@test.com",
            "firstname": "test_adminplatform_doctor3_firstname",
            "lastname": "test_adminplatform_doctor3_lastname",
        },
        {
            "type_2fa": Type2FA.EMAIL.value,
            "licence_type": TypeLicenceEnum.MEDICAL_STAFF.value,
            "email": "test_adminplatform_medicalstaff2@test.com",
            "firstname": "test_adminplatform_medicalstaff2_firstname",
            "lastname": "test_adminplatform_medicalstaff2_lastname",
        },
        {
            "type_2fa": Type2FA.EMAIL.value,
            "licence_type": TypeLicenceEnum.MEDICAL_STAFF.value,
            "email": "test_adminplatform_medicalstaff3@test.com",
            "firstname": "test_adminplatform_medicalstaff3_firstname",
            "lastname": "test_adminplatform_medicalstaff3_lastname",
        },
    ]

    response = await client.get(
            f"/orders/{UUID_ORDER_3}/users",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == []

    response = await client.get(
            f"/orders/{UUID_ORDER_4}/users",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_get_order_users_from_local_admin(client: AsyncClient, session: AsyncSession) -> None:
    await pre_fill_db(session)
    response = await client.get(
            f"/orders/{UUID_ORDER_1}/users",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == [
        {
            "type_2fa": Type2FA.EMAIL.value,
            "licence_type": TypeLicenceEnum.DOCTOR.value,
            "email": "test_adminplatform_doctor1@test.com",
            "firstname": "test_adminplatform_doctor1_firstname",
            "lastname": "test_adminplatform_doctor1_lastname",
        },
        {
            "type_2fa": Type2FA.EMAIL.value,
            "licence_type": TypeLicenceEnum.DOCTOR.value,
            "email": "test_adminplatform_doctor2@test.com",
            "firstname": "test_adminplatform_doctor2_firstname",
            "lastname": "test_adminplatform_doctor2_lastname",
        },
        {
            "type_2fa": Type2FA.EMAIL.value,
            "licence_type": TypeLicenceEnum.MEDICAL_STAFF.value,
            "email": "test_adminplatform_medicalstaff1@test.com",
            "firstname": "test_adminplatform_medicalstaff1_firstname",
            "lastname": "test_adminplatform_medicalstaff1_lastname",
        },
    ]

    response = await client.get(
            f"/orders/{UUID_ORDER_2}/users",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == [
        {
            "type_2fa": Type2FA.EMAIL.value,
            "licence_type": TypeLicenceEnum.DOCTOR.value,
            "email": "test_adminplatform_doctor3@test.com",
            "firstname": "test_adminplatform_doctor3_firstname",
            "lastname": "test_adminplatform_doctor3_lastname",
        },
        {
            "type_2fa": Type2FA.EMAIL.value,
            "licence_type": TypeLicenceEnum.MEDICAL_STAFF.value,
            "email": "test_adminplatform_medicalstaff2@test.com",
            "firstname": "test_adminplatform_medicalstaff2_firstname",
            "lastname": "test_adminplatform_medicalstaff2_lastname",
        },
        {
            "type_2fa": Type2FA.EMAIL.value,
            "licence_type": TypeLicenceEnum.MEDICAL_STAFF.value,
            "email": "test_adminplatform_medicalstaff3@test.com",
            "firstname": "test_adminplatform_medicalstaff3_firstname",
            "lastname": "test_adminplatform_medicalstaff3_lastname",
        },
    ]

    response = await client.get(
            f"/orders/{UUID_ORDER_4}/users",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_get_order_users_from_local_admin_forbidden(client: AsyncClient, session: AsyncSession) -> None:
    await pre_fill_db(session)

    response = await client.get(
            f"/orders/{UUID_ORDER_3}/users",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}
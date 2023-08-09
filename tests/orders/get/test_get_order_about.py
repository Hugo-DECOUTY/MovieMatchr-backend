import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from adminplatform.schemas.account.user import Type2FA
from adminplatform.schemas.licences.licences import TypeLicenceEnum

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
async def test_get_order_about_from_admin(client: AsyncClient, session: AsyncSession) -> None:
    await pre_fill_db(session)
    response = await client.get(
            f"/orders/{UUID_ORDER_1}/about",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == {
            "local_admin": {
                "email": "local-admin@test.com",
                "firstname": "Local",
                "lastname": "Admin",
            },
            "users": [
                {
                    "type_2fa": Type2FA.EMAIL.value,
                    "licence_type": TypeLicenceEnum.DOCTOR.value,
                    "id_licence": "e227d564-3238-473c-aff7-630bdcd6cfd1",
                    "email": "test_adminplatform_doctor1@test.com",
                    "firstname": "test_adminplatform_doctor1_firstname",
                    "lastname": "test_adminplatform_doctor1_lastname",
                },
                {
                    "type_2fa": Type2FA.EMAIL.value,
                    "licence_type": TypeLicenceEnum.DOCTOR.value,
                    "id_licence": "e227d564-3238-473c-aff7-630bdcd6cfd2",
                    "email": "test_adminplatform_doctor2@test.com",
                    "firstname": "test_adminplatform_doctor2_firstname",
                    "lastname": "test_adminplatform_doctor2_lastname",
                },
                {
                    "type_2fa": Type2FA.EMAIL.value,
                    "licence_type": TypeLicenceEnum.MEDICAL_STAFF.value,
                    "id_licence": "e227d564-3238-473c-aff7-630bdcd6cfd4",
                    "email": "test_adminplatform_medicalstaff1@test.com",
                    "firstname": "test_adminplatform_medicalstaff1_firstname",
                    "lastname": "test_adminplatform_medicalstaff1_lastname",
                },
            ],
            "seller": {
                "email": "seller1@gmail.com",
                "firstname": "Seller1FirstName",
                "lastname": "Seller1LastName",
                "phone": None,
            },
            "sum_of_recording_analyzed_in_order": 0,
        }

    response = await client.get(
            f"/orders/{UUID_ORDER_2}/about",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == {
            "local_admin": {
                "email": "local-admin@test.com",
                "firstname": "Local",
                "lastname": "Admin",
            },
            "users": [
                {
                    "type_2fa": Type2FA.EMAIL.value,
                    "licence_type": TypeLicenceEnum.DOCTOR.value,
                    "id_licence": "e227d564-3238-473c-aff7-630bdcd6cfd3",
                    "email": "test_adminplatform_doctor3@test.com",
                    "firstname": "test_adminplatform_doctor3_firstname",
                    "lastname": "test_adminplatform_doctor3_lastname",
                },
                {
                    "type_2fa": Type2FA.EMAIL.value,
                    "licence_type": TypeLicenceEnum.MEDICAL_STAFF.value,
                    "id_licence": "e227d564-3238-473c-aff7-630bdcd6cfd5",
                    "email": "test_adminplatform_medicalstaff2@test.com",
                    "firstname": "test_adminplatform_medicalstaff2_firstname",
                    "lastname": "test_adminplatform_medicalstaff2_lastname",
                },
                {
                    "type_2fa": Type2FA.EMAIL.value,
                    "licence_type": TypeLicenceEnum.MEDICAL_STAFF.value,
                    "id_licence": "e227d564-3238-473c-aff7-630bdcd6cfd6",
                    "email": "test_adminplatform_medicalstaff3@test.com",
                    "firstname": "test_adminplatform_medicalstaff3_firstname",
                    "lastname": "test_adminplatform_medicalstaff3_lastname",
                },
            ],
            "seller": {
                "email": "seller1@gmail.com",
                "firstname": "Seller1FirstName",
                "lastname": "Seller1LastName",
                "phone": None,
            },
            "sum_of_recording_analyzed_in_order": 0,
        }

    response = await client.get(
            f"/orders/{UUID_ORDER_3}/about",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == {
            "local_admin": {
                "email": "hds-admin-microport@test.com",
                "firstname": "HDS",
                "lastname": "Admin",
            },
            "users": [],
            "seller": {
                "email": "seller1@gmail.com",
                "firstname": "Seller1FirstName",
                "lastname": "Seller1LastName",
                "phone": None,
            },
            "sum_of_recording_analyzed_in_order": 0,
        }

    response = await client.get(
            f"/orders/{UUID_ORDER_4}/about",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == {
            "local_admin": {
                "email": "local-admin@test.com",
                "firstname": "Local",
                "lastname": "Admin",
            },
            "users": [],
            "seller": {
                "email": "seller1@gmail.com",
                "firstname": "Seller1FirstName",
                "lastname": "Seller1LastName",
                "phone": None,
            },
            "sum_of_recording_analyzed_in_order": 0,
        }

@pytest.mark.asyncio
async def test_get_order_about_from_local_admin_forbidden(client: AsyncClient, session: AsyncSession) -> None:
    await pre_fill_db(session)

    response = await client.get(
            f"/orders/{UUID_ORDER_1}/about",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.get(
            f"/orders/{UUID_ORDER_2}/about",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.get(
            f"/orders/{UUID_ORDER_3}/about",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.get(
            f"/orders/{UUID_ORDER_4}/about",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}
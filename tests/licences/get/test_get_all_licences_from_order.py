import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from adminplatform.schemas.licences.licences import TypeLicenceEnum
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
    UUID_LICENCE_1,
    UUID_LICENCE_2,
    UUID_LICENCE_3,
    UUID_LICENCE_4,
    UUID_LICENCE_5,
    UUID_LICENCE_6,
    SERIAL_LICENCE_1,
    SERIAL_LICENCE_2,
    SERIAL_LICENCE_3,
    SERIAL_LICENCE_4,
    SERIAL_LICENCE_5,
    SERIAL_LICENCE_6,
    UNUSED_UUID_LICENCE_1,
    UNUSED_UUID_LICENCE_2,
    UNUSED_UUID_LICENCE_3,
    UNUSED_UUID_LICENCE_4,
    UNUSED_UUID_LICENCE_5,
    UNUSED_UUID_LICENCE_6,
    UNUSED_UUID_LICENCE_7,
    UNUSED_UUID_LICENCE_8,
    UNUSED_UUID_LICENCE_9,
    UNUSED_UUID_LICENCE_10,
    UNUSED_UUID_LICENCE_11,
    UNUSED_UUID_LICENCE_12,
    UNUSED_UUID_LICENCE_13,
    UNUSED_SERIAL_LICENCE_1,
    UNUSED_SERIAL_LICENCE_2,
    UNUSED_SERIAL_LICENCE_3,
    UNUSED_SERIAL_LICENCE_4,
    UNUSED_SERIAL_LICENCE_5,
    UNUSED_SERIAL_LICENCE_6,
    UNUSED_SERIAL_LICENCE_7,
    UNUSED_SERIAL_LICENCE_8,
    UNUSED_SERIAL_LICENCE_9,
    UNUSED_SERIAL_LICENCE_10,
    UNUSED_SERIAL_LICENCE_11,
    UNUSED_SERIAL_LICENCE_12,
    UNUSED_SERIAL_LICENCE_13,
    USER_LICENCE_ID_1,
    USER_LICENCE_ID_2,
    USER_LICENCE_ID_3,
    USER_LICENCE_ID_4,
    USER_LICENCE_ID_5,
    USER_LICENCE_ID_6,
    pre_fill_db,
)

@pytest.mark.asyncio
async def test_get_all_licences_from_order_from_admin(client: AsyncClient, session: AsyncSession) -> None:
    await pre_fill_db(session)
    response = await client.get(
            f"/licences/{UUID_ORDER_NOT_FOUND}",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN}
        )
    assert response.status_code == 404
    assert response.json() == {"detail": HttpErrorsEnum.ORDER_NOT_FOUND.value}

    response = await client.get(
            f"/licences/{UUID_ORDER_1}",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": UUID_LICENCE_1,
            "licence_type": TypeLicenceEnum.DOCTOR.value,
            "serial_number": SERIAL_LICENCE_1,
            "id_order": UUID_ORDER_1,
            "id_user": USER_LICENCE_ID_1,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
        {
            "id": UUID_LICENCE_2,
            "licence_type": TypeLicenceEnum.DOCTOR.value,
            "serial_number": SERIAL_LICENCE_2,
            "id_order": UUID_ORDER_1,
            "id_user": USER_LICENCE_ID_2,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
        {
            "id": UUID_LICENCE_4,
            "licence_type": TypeLicenceEnum.MEDICAL_STAFF.value,
            "serial_number": SERIAL_LICENCE_4,
            "id_order": UUID_ORDER_1,
            "id_user": USER_LICENCE_ID_4,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
        {
            "id": UNUSED_UUID_LICENCE_1,
            "licence_type": None,
            "serial_number": UNUSED_SERIAL_LICENCE_1,
            "id_order": UUID_ORDER_1,
            "id_user": None,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
        {
            "id": UNUSED_UUID_LICENCE_2,
            "licence_type": None,
            "serial_number": UNUSED_SERIAL_LICENCE_2,
            "id_order": UUID_ORDER_1,
            "id_user": None,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
        {
            "id": UNUSED_UUID_LICENCE_3,
            "licence_type": None,
            "serial_number": UNUSED_SERIAL_LICENCE_3,
            "id_order": UUID_ORDER_1,
            "id_user": None,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
        {
            "id": UNUSED_UUID_LICENCE_4,
            "licence_type": None,
            "serial_number": UNUSED_SERIAL_LICENCE_4,
            "id_order": UUID_ORDER_1,
            "id_user": None,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
        {
            "id": UNUSED_UUID_LICENCE_5,
            "licence_type": None,
            "serial_number": UNUSED_SERIAL_LICENCE_5,
            "id_order": UUID_ORDER_1,
            "id_user": None,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
    ]

    response = await client.get(
            f"/licences/{UUID_ORDER_2}",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": UUID_LICENCE_3,
            "licence_type": TypeLicenceEnum.DOCTOR.value,
            "serial_number": SERIAL_LICENCE_3,
            "id_order": UUID_ORDER_2,
            "id_user": USER_LICENCE_ID_3,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
        {
            "id": UUID_LICENCE_5,
            "licence_type": TypeLicenceEnum.MEDICAL_STAFF.value,
            "serial_number": SERIAL_LICENCE_5,
            "id_order": UUID_ORDER_2,
            "id_user": USER_LICENCE_ID_5,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
        {
            "id": UUID_LICENCE_6,
            "licence_type": TypeLicenceEnum.MEDICAL_STAFF.value,
            "serial_number": SERIAL_LICENCE_6,
            "id_order": UUID_ORDER_2,
            "id_user": USER_LICENCE_ID_6,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
        {
            "id": UNUSED_UUID_LICENCE_6,
            "licence_type": None,
            "serial_number": UNUSED_SERIAL_LICENCE_6,
            "id_order": UUID_ORDER_2,
            "id_user": None,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
        {
            "id": UNUSED_UUID_LICENCE_7,
            "licence_type": None,
            "serial_number": UNUSED_SERIAL_LICENCE_7,
            "id_order": UUID_ORDER_2,
            "id_user": None,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
        {
            "id": UNUSED_UUID_LICENCE_8,
            "licence_type": None,
            "serial_number": UNUSED_SERIAL_LICENCE_8,
            "id_order": UUID_ORDER_2,
            "id_user": None,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
    ]

    response = await client.get(
            f"/licences/{UUID_ORDER_3}",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": UNUSED_UUID_LICENCE_9,
            "licence_type": None,
            "serial_number": UNUSED_SERIAL_LICENCE_9,
            "id_order": UUID_ORDER_3,
            "id_user": None,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
        {
            "id": UNUSED_UUID_LICENCE_10,
            "licence_type": None,
            "serial_number": UNUSED_SERIAL_LICENCE_10,
            "id_order": UUID_ORDER_3,
            "id_user": None,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
    ]

    response = await client.get(
            f"/licences/{UUID_ORDER_4}",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": UNUSED_UUID_LICENCE_11,
            "licence_type": None,
            "serial_number": UNUSED_SERIAL_LICENCE_11,
            "id_order": UUID_ORDER_4,
            "id_user": None,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
        {
            "id": UNUSED_UUID_LICENCE_12,
            "licence_type": None,
            "serial_number": UNUSED_SERIAL_LICENCE_12,
            "id_order": UUID_ORDER_4,
            "id_user": None,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
        {
            "id": UNUSED_UUID_LICENCE_13,
            "licence_type": None,
            "serial_number": UNUSED_SERIAL_LICENCE_13,
            "id_order": UUID_ORDER_4,
            "id_user": None,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
    ]

@pytest.mark.asyncio
async def test_get_all_licences_from_order_from_local_admin(client: AsyncClient, session: AsyncSession) -> None:
    await pre_fill_db(session)
    response = await client.get(
            f"/licences/{UUID_ORDER_NOT_FOUND}",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN}
        )
    assert response.status_code == 404
    assert response.json() == {"detail": HttpErrorsEnum.ORDER_NOT_FOUND.value}

    response = await client.get(
            f"/licences/{UUID_ORDER_1}",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": UUID_LICENCE_1,
            "licence_type": TypeLicenceEnum.DOCTOR.value,
            "serial_number": SERIAL_LICENCE_1,
            "id_order": UUID_ORDER_1,
            "id_user": USER_LICENCE_ID_1,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
        {
            "id": UUID_LICENCE_2,
            "licence_type": TypeLicenceEnum.DOCTOR.value,
            "serial_number": SERIAL_LICENCE_2,
            "id_order": UUID_ORDER_1,
            "id_user": USER_LICENCE_ID_2,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
        {
            "id": UUID_LICENCE_4,
            "licence_type": TypeLicenceEnum.MEDICAL_STAFF.value,
            "serial_number": SERIAL_LICENCE_4,
            "id_order": UUID_ORDER_1,
            "id_user": USER_LICENCE_ID_4,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
        {
            "id": UNUSED_UUID_LICENCE_1,
            "licence_type": None,
            "serial_number": UNUSED_SERIAL_LICENCE_1,
            "id_order": UUID_ORDER_1,
            "id_user": None,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
        {
            "id": UNUSED_UUID_LICENCE_2,
            "licence_type": None,
            "serial_number": UNUSED_SERIAL_LICENCE_2,
            "id_order": UUID_ORDER_1,
            "id_user": None,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
        {
            "id": UNUSED_UUID_LICENCE_3,
            "licence_type": None,
            "serial_number": UNUSED_SERIAL_LICENCE_3,
            "id_order": UUID_ORDER_1,
            "id_user": None,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
        {
            "id": UNUSED_UUID_LICENCE_4,
            "licence_type": None,
            "serial_number": UNUSED_SERIAL_LICENCE_4,
            "id_order": UUID_ORDER_1,
            "id_user": None,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
        {
            "id": UNUSED_UUID_LICENCE_5,
            "licence_type": None,
            "serial_number": UNUSED_SERIAL_LICENCE_5,
            "id_order": UUID_ORDER_1,
            "id_user": None,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
    ]

    response = await client.get(
            f"/licences/{UUID_ORDER_2}",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": UUID_LICENCE_3,
            "licence_type": TypeLicenceEnum.DOCTOR.value,
            "serial_number": SERIAL_LICENCE_3,
            "id_order": UUID_ORDER_2,
            "id_user": USER_LICENCE_ID_3,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
        {
            "id": UUID_LICENCE_5,
            "licence_type": TypeLicenceEnum.MEDICAL_STAFF.value,
            "serial_number": SERIAL_LICENCE_5,
            "id_order": UUID_ORDER_2,
            "id_user": USER_LICENCE_ID_5,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
        {
            "id": UUID_LICENCE_6,
            "licence_type": TypeLicenceEnum.MEDICAL_STAFF.value,
            "serial_number": SERIAL_LICENCE_6,
            "id_order": UUID_ORDER_2,
            "id_user": USER_LICENCE_ID_6,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
        {
            "id": UNUSED_UUID_LICENCE_6,
            "licence_type": None,
            "serial_number": UNUSED_SERIAL_LICENCE_6,
            "id_order": UUID_ORDER_2,
            "id_user": None,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
        {
            "id": UNUSED_UUID_LICENCE_7,
            "licence_type": None,
            "serial_number": UNUSED_SERIAL_LICENCE_7,
            "id_order": UUID_ORDER_2,
            "id_user": None,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
        {
            "id": UNUSED_UUID_LICENCE_8,
            "licence_type": None,
            "serial_number": UNUSED_SERIAL_LICENCE_8,
            "id_order": UUID_ORDER_2,
            "id_user": None,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
    ]

    response = await client.get(
            f"/licences/{UUID_ORDER_4}",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": UNUSED_UUID_LICENCE_11,
            "licence_type": None,
            "serial_number": UNUSED_SERIAL_LICENCE_11,
            "id_order": UUID_ORDER_4,
            "id_user": None,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
        {
            "id": UNUSED_UUID_LICENCE_12,
            "licence_type": None,
            "serial_number": UNUSED_SERIAL_LICENCE_12,
            "id_order": UUID_ORDER_4,
            "id_user": None,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
        {
            "id": UNUSED_UUID_LICENCE_13,
            "licence_type": None,
            "serial_number": UNUSED_SERIAL_LICENCE_13,
            "id_order": UUID_ORDER_4,
            "id_user": None,
            "nb_recording_analyzed": 0,
            "demo_flag": False,
            "active": True,
        },
    ]

@pytest.mark.asyncio
async def test_get_all_licences_from_order_from_local_admin_forbidden(client: AsyncClient, session: AsyncSession) -> None:
    await pre_fill_db(session)
    response = await client.get(
            f"/licences/{UUID_ORDER_3}",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": HttpErrorsEnum.YOU_DO_NOT_OWN_THIS_ORDER.value}

@pytest.mark.asyncio
async def test_get_all_licences_from_order_from_unknown_user_forbidden(client: AsyncClient, session: AsyncSession) -> None:
    await pre_fill_db(session)
    response = await client.get(
            f"/licences/{UUID_ORDER_NOT_FOUND}",
            headers={"X-USERINFO": ACCESS_TOKEN_UNKNOWN_USER}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.get(
            f"/licences/{UUID_ORDER_1}",
            headers={"X-USERINFO": ACCESS_TOKEN_UNKNOWN_USER}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.get(
            f"/licences/{UUID_ORDER_2}",
            headers={"X-USERINFO": ACCESS_TOKEN_UNKNOWN_USER}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.get(
            f"/licences/{UUID_ORDER_3}",
            headers={"X-USERINFO": ACCESS_TOKEN_UNKNOWN_USER}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.get(
            f"/licences/{UUID_ORDER_4}",
            headers={"X-USERINFO": ACCESS_TOKEN_UNKNOWN_USER}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

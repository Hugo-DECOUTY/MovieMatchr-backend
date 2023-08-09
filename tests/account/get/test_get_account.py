import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from adminplatform.enum.errors.HttpErrorsEnum import HttpErrorsEnum

from tests.conftest import pre_fill_db

from tests.conftest import (
    ACCESS_TOKEN_ADMIN,
    ACCESS_TOKEN_LOCAL_ADMIN,
    ACCESS_TOKEN_UNKNOWN_USER,
    UUID_ADMIN,
    UUID_MICROPORT_STAFF,
    UUID_LOCAL_ADMIN,
)

UUID_USER = "30127b9f-2dd9-4771-b040-91a4f3c359c0"

@pytest.mark.asyncio
async def test_get_account_from_admin(client: AsyncClient, session: AsyncSession) -> None:
    await pre_fill_db(session)
    response = await client.get(
            f"/account/{'123'}",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN}
        )
    assert response.status_code == 404
    assert response.json() == {"detail": HttpErrorsEnum.USER_NOT_FOUND.value}

    response = await client.get(
            f"/account/{UUID_ADMIN}",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == {
        "id": UUID_ADMIN,
        "email": "hds-admin-microport@test.com",
        "first_name": "HDS",
        "last_name": "Admin",
    }

    response = await client.get(
            f"/account/{UUID_MICROPORT_STAFF}",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == {
        "id": UUID_MICROPORT_STAFF,
        "email": "microport-staff@test.com",
        "first_name": "Microport-staff",
        "last_name": "Test",
    }

    response = await client.get(
            f"/account/{UUID_LOCAL_ADMIN}",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == {
        "id": UUID_LOCAL_ADMIN,
        "email": "local-admin@test.com",
        "first_name": "Local",
        "last_name": "Admin",
    }

    response = await client.get(
            f"/account/{UUID_USER}",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == {
        "id": UUID_USER,
        "email": "non-medical-staff@test.com",
        "first_name": "Non-medical-staff",
        "last_name": "Test",
    }

@pytest.mark.asyncio
async def test_get_account_from_local_admin(client: AsyncClient, session: AsyncSession) -> None:
    await pre_fill_db(session)
    response = await client.get(
            f"/account/{'123'}",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN}
        )
    assert response.status_code == 404
    assert response.json() == {"detail": HttpErrorsEnum.USER_NOT_FOUND.value}

    response = await client.get(
            f"/account/{UUID_ADMIN}",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == {
        "id": UUID_ADMIN,
        "email": "hds-admin-microport@test.com",
        "first_name": "HDS",
        "last_name": "Admin",
    }

    response = await client.get(
            f"/account/{UUID_MICROPORT_STAFF}",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == {
        "id": UUID_MICROPORT_STAFF,
        "email": "microport-staff@test.com",
        "first_name": "Microport-staff",
        "last_name": "Test",
    }

    response = await client.get(
            f"/account/{UUID_LOCAL_ADMIN}",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == {
        "id": UUID_LOCAL_ADMIN,
        "email": "local-admin@test.com",
        "first_name": "Local",
        "last_name": "Admin",
    }

    response = await client.get(
            f"/account/{UUID_USER}",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == {
        "id": UUID_USER,
        "email": "non-medical-staff@test.com",
        "first_name": "Non-medical-staff",
        "last_name": "Test",
    }

@pytest.mark.asyncio
async def test_get_account_from_unknown_user_forbidden(client: AsyncClient, session: AsyncSession) -> None:
    await pre_fill_db(session)
    response = await client.get(
            f"/account/{'123'}",
            headers={"X-USERINFO": ACCESS_TOKEN_UNKNOWN_USER}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.get(
            f"/account/{UUID_ADMIN}",
            headers={"X-USERINFO": ACCESS_TOKEN_UNKNOWN_USER}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.get(
            f"/account/{UUID_MICROPORT_STAFF}",
            headers={"X-USERINFO": ACCESS_TOKEN_UNKNOWN_USER}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.get(
            f"/account/{UUID_LOCAL_ADMIN}",
            headers={"X-USERINFO": ACCESS_TOKEN_UNKNOWN_USER}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.get(
            f"/account/{UUID_USER}",
            headers={"X-USERINFO": ACCESS_TOKEN_UNKNOWN_USER}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

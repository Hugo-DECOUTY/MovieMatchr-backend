import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from moviematchr.enum.errors.HttpErrorsEnum import HttpErrorsEnum

from tests.conftest import (
    ACCESS_TOKEN_ADMIN,
    ACCESS_TOKEN_LOCAL_ADMIN,
    ACCESS_TOKEN_UNKNOWN_USER,
    UUID_SELLER_NOT_FOUND,
    UUID_SELLER_1,
    UUID_SELLER_2,
    UUID_SELLER_3,
    UUID_SELLER_4,
    pre_fill_db,
)


@pytest.mark.asyncio
async def test_get_one_seller_from_admin(client: AsyncClient, session: AsyncSession) -> None:
    await pre_fill_db(session)
    response = await client.get(
            f"/sellers/{UUID_SELLER_NOT_FOUND}",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN}
        )
    assert response.status_code == 404
    assert response.json() == {"detail": HttpErrorsEnum.SELLER_NOT_FOUND.value}

    response = await client.get(
            f"/sellers/{UUID_SELLER_1}",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == {
            "id": UUID_SELLER_1,
            "email": "seller1@gmail.com",
            "firstname": "Seller1FirstName",
            "lastname": "Seller1LastName",
            "phone": None,
        }

    response = await client.get(
            f"/sellers/{UUID_SELLER_2}",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == {
            "id": UUID_SELLER_2,
            "email": "seller2@gmail.com",
            "firstname": "Seller2FirstName",
            "lastname": "Seller2LastName",
            "phone": None,
        }

    response = await client.get(
            f"/sellers/{UUID_SELLER_3}",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == {
            "id": UUID_SELLER_3,
            "email": "seller3@gmail.com",
            "firstname": "Seller3FirstName",
            "lastname": "Seller3LastName",
            "phone": None,
        }

    response = await client.get(
            f"/sellers/{UUID_SELLER_4}",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN}
        )
    assert response.status_code == 200
    assert response.json() == {
            "id": UUID_SELLER_4,
            "email": "seller4@gmail.com",
            "firstname": "Seller4FirstName",
            "lastname": "Seller4LastName",
            "phone": None,
        }

@pytest.mark.asyncio
async def test_get_one_seller_from_local_admin_forbidden(client: AsyncClient, session: AsyncSession) -> None:
    await pre_fill_db(session)
    response = await client.get(
            f"/sellers/{UUID_SELLER_NOT_FOUND}",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.get(
            f"/sellers/{UUID_SELLER_1}",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.get(
            f"/sellers/{UUID_SELLER_2}",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.get(
            f"/sellers/{UUID_SELLER_3}",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.get(
            f"/sellers/{UUID_SELLER_4}",
            headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

@pytest.mark.asyncio
async def test_get_one_seller_from_unknwon_user_forbidden(client: AsyncClient, session: AsyncSession) -> None:
    await pre_fill_db(session)
    response = await client.get(
            f"/sellers/{UUID_SELLER_NOT_FOUND}",
            headers={"X-USERINFO": ACCESS_TOKEN_UNKNOWN_USER}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.get(
            f"/sellers/{UUID_SELLER_1}",
            headers={"X-USERINFO": ACCESS_TOKEN_UNKNOWN_USER}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.get(
            f"/sellers/{UUID_SELLER_2}",
            headers={"X-USERINFO": ACCESS_TOKEN_UNKNOWN_USER}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.get(
            f"/sellers/{UUID_SELLER_3}",
            headers={"X-USERINFO": ACCESS_TOKEN_UNKNOWN_USER}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.get(
            f"/sellers/{UUID_SELLER_4}",
            headers={"X-USERINFO": ACCESS_TOKEN_UNKNOWN_USER}
        )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}
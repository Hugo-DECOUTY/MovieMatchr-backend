import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from moviematchr.schemas.orders.orders import StateOrderEnum
from moviematchr.enum.errors.HttpErrorsEnum import HttpErrorsEnum

from tests.conftest import (
    ACCESS_TOKEN_ADMIN,
    ACCESS_TOKEN_LOCAL_ADMIN,
    ACCESS_TOKEN_UNKNOWN_USER,
    UUID_ADMIN,
    UUID_LOCAL_ADMIN,
    UUID_ORDER_NOT_FOUND,
    UUID_ORDER_1,
    UUID_ORDER_2,
    UUID_ORDER_3,
    UUID_ORDER_4,
    UUID_SELLER_1,
    pre_fill_db,
)


@pytest.mark.asyncio
async def test_delete_one_order_from_admin(
    client: AsyncClient, session: AsyncSession
) -> None:
    await pre_fill_db(session)
    response = await client.get("/orders", headers={"X-USERINFO": ACCESS_TOKEN_ADMIN})
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": UUID_ORDER_1,
            "order_id": "#0000000001",
            "local_admin_id": UUID_LOCAL_ADMIN,
            "nb_shared_tokens": 0,
            "billing_type": None,
            "country": "France",
            "workplace": "Gotham",
            "service": "Cardiologie",
            "seller_id": UUID_SELLER_1,
            "state_flag": StateOrderEnum.ACCEPTED.value,
            "sending_date": 1666870958,
            "order_accepted_date": 1666870958,
            "demo_flag": False,
            "sharing_authorization": True,
            "company_only": False,
        },
        {
            "id": UUID_ORDER_2,
            "order_id": "#0000000002",
            "local_admin_id": UUID_LOCAL_ADMIN,
            "nb_shared_tokens": 0,
            "billing_type": None,
            "country": "France",
            "workplace": "La Rochelle",
            "service": "Cardiologie",
            "seller_id": UUID_SELLER_1,
            "state_flag": StateOrderEnum.ACCEPTED.value,
            "sending_date": 1666870958,
            "order_accepted_date": 1666870958,
            "demo_flag": False,
            "sharing_authorization": True,
            "company_only": False,
        },
        {
            "id": UUID_ORDER_3,
            "order_id": "#0000000003",
            "local_admin_id": UUID_ADMIN,
            "nb_shared_tokens": 0,
            "billing_type": None,
            "country": "France",
            "workplace": "Royan",
            "service": "Cardiologie",
            "seller_id": UUID_SELLER_1,
            "state_flag": StateOrderEnum.ACCEPTED.value,
            "sending_date": 1666870958,
            "order_accepted_date": 1666870958,
            "demo_flag": False,
            "sharing_authorization": True,
            "company_only": False,
        },
        {
            "id": UUID_ORDER_4,
            "order_id": "#0000000004",
            "local_admin_id": UUID_LOCAL_ADMIN,
            "nb_shared_tokens": 0,
            "billing_type": None,
            "country": "France",
            "workplace": "Paris",
            "service": "Cardiologie",
            "seller_id": UUID_SELLER_1,
            "state_flag": StateOrderEnum.EXPIRED.value,
            "sending_date": 1666870958,
            "order_accepted_date": 1666870958,
            "demo_flag": True,
            "sharing_authorization": True,
            "company_only": False,
        },
    ]

    response = await client.delete(
        f"/orders/{UUID_ORDER_4}", headers={"X-USERINFO": ACCESS_TOKEN_ADMIN}
    )
    assert response.status_code == 200

    response = await client.get("/orders", headers={"X-USERINFO": ACCESS_TOKEN_ADMIN})
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": UUID_ORDER_1,
            "order_id": "#0000000001",
            "local_admin_id": UUID_LOCAL_ADMIN,
            "nb_shared_tokens": 0,
            "billing_type": None,
            "country": "France",
            "workplace": "Gotham",
            "service": "Cardiologie",
            "seller_id": UUID_SELLER_1,
            "state_flag": StateOrderEnum.ACCEPTED.value,
            "sending_date": 1666870958,
            "order_accepted_date": 1666870958,
            "demo_flag": False,
            "sharing_authorization": True,
            "company_only": False,
        },
        {
            "id": UUID_ORDER_2,
            "order_id": "#0000000002",
            "local_admin_id": UUID_LOCAL_ADMIN,
            "nb_shared_tokens": 0,
            "billing_type": None,
            "country": "France",
            "workplace": "La Rochelle",
            "service": "Cardiologie",
            "seller_id": UUID_SELLER_1,
            "state_flag": StateOrderEnum.ACCEPTED.value,
            "sending_date": 1666870958,
            "order_accepted_date": 1666870958,
            "demo_flag": False,
            "sharing_authorization": True,
            "company_only": False,
        },
        {
            "id": UUID_ORDER_3,
            "order_id": "#0000000003",
            "local_admin_id": UUID_ADMIN,
            "nb_shared_tokens": 0,
            "billing_type": None,
            "country": "France",
            "workplace": "Royan",
            "service": "Cardiologie",
            "seller_id": UUID_SELLER_1,
            "state_flag": StateOrderEnum.ACCEPTED.value,
            "sending_date": 1666870958,
            "order_accepted_date": 1666870958,
            "demo_flag": False,
            "sharing_authorization": True,
            "company_only": False,
        },
        {
            "id": UUID_ORDER_4,
            "order_id": "#0000000004",
            "local_admin_id": UUID_LOCAL_ADMIN,
            "nb_shared_tokens": 0,
            "billing_type": None,
            "country": "France",
            "workplace": "Paris",
            "service": "Cardiologie",
            "seller_id": UUID_SELLER_1,
            "state_flag": StateOrderEnum.DELETED.value,
            "sending_date": 1666870958,
            "order_accepted_date": 1666870958,
            "demo_flag": True,
            "sharing_authorization": True,
            "company_only": False,
        },
    ]

    response = await client.delete(
        f"/orders/{UUID_ORDER_2}", headers={"X-USERINFO": ACCESS_TOKEN_ADMIN}
    )
    assert response.status_code == 200

    response = await client.get("/orders", headers={"X-USERINFO": ACCESS_TOKEN_ADMIN})
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": UUID_ORDER_1,
            "order_id": "#0000000001",
            "local_admin_id": UUID_LOCAL_ADMIN,
            "nb_shared_tokens": 0,
            "billing_type": None,
            "country": "France",
            "workplace": "Gotham",
            "service": "Cardiologie",
            "seller_id": UUID_SELLER_1,
            "state_flag": StateOrderEnum.ACCEPTED.value,
            "sending_date": 1666870958,
            "order_accepted_date": 1666870958,
            "demo_flag": False,
            "sharing_authorization": True,
            "company_only": False,
        },
        {
            "id": UUID_ORDER_2,
            "order_id": "#0000000002",
            "local_admin_id": UUID_LOCAL_ADMIN,
            "nb_shared_tokens": 0,
            "billing_type": None,
            "country": "France",
            "workplace": "La Rochelle",
            "service": "Cardiologie",
            "seller_id": UUID_SELLER_1,
            "state_flag": StateOrderEnum.DELETED.value,
            "sending_date": 1666870958,
            "order_accepted_date": 1666870958,
            "demo_flag": False,
            "sharing_authorization": True,
            "company_only": False,
        },
        {
            "id": UUID_ORDER_3,
            "order_id": "#0000000003",
            "local_admin_id": UUID_ADMIN,
            "nb_shared_tokens": 0,
            "billing_type": None,
            "country": "France",
            "workplace": "Royan",
            "service": "Cardiologie",
            "seller_id": UUID_SELLER_1,
            "state_flag": StateOrderEnum.ACCEPTED.value,
            "sending_date": 1666870958,
            "order_accepted_date": 1666870958,
            "demo_flag": False,
            "sharing_authorization": True,
            "company_only": False,
        },
        {
            "id": UUID_ORDER_4,
            "order_id": "#0000000004",
            "local_admin_id": UUID_LOCAL_ADMIN,
            "nb_shared_tokens": 0,
            "billing_type": None,
            "country": "France",
            "workplace": "Paris",
            "service": "Cardiologie",
            "seller_id": UUID_SELLER_1,
            "state_flag": StateOrderEnum.DELETED.value,
            "sending_date": 1666870958,
            "order_accepted_date": 1666870958,
            "demo_flag": True,
            "sharing_authorization": True,
            "company_only": False,
        },
    ]

    response = await client.delete(
        f"/orders/{UUID_ORDER_NOT_FOUND}", headers={"X-USERINFO": ACCESS_TOKEN_ADMIN}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": HttpErrorsEnum.ORDER_NOT_FOUND.value}


@pytest.mark.asyncio
async def test_delete_one_order_from_local_admin_forbidden(
    client: AsyncClient, session: AsyncSession
) -> None:
    await pre_fill_db(session)
    response = await client.get(
        "/orders", headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN}
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": UUID_ORDER_1,
            "order_id": "#0000000001",
            "local_admin_id": UUID_LOCAL_ADMIN,
            "nb_shared_tokens": 0,
            "billing_type": None,
            "country": "France",
            "workplace": "Gotham",
            "service": "Cardiologie",
            "seller_id": UUID_SELLER_1,
            "state_flag": StateOrderEnum.ACCEPTED.value,
            "sending_date": 1666870958,
            "order_accepted_date": 1666870958,
            "demo_flag": False,
            "sharing_authorization": True,
            "company_only": False,
        },
        {
            "id": UUID_ORDER_2,
            "order_id": "#0000000002",
            "local_admin_id": UUID_LOCAL_ADMIN,
            "nb_shared_tokens": 0,
            "billing_type": None,
            "country": "France",
            "workplace": "La Rochelle",
            "service": "Cardiologie",
            "seller_id": UUID_SELLER_1,
            "state_flag": StateOrderEnum.ACCEPTED.value,
            "sending_date": 1666870958,
            "order_accepted_date": 1666870958,
            "demo_flag": False,
            "sharing_authorization": True,
            "company_only": False,
        },
        {
            "id": UUID_ORDER_4,
            "order_id": "#0000000004",
            "local_admin_id": UUID_LOCAL_ADMIN,
            "nb_shared_tokens": 0,
            "billing_type": None,
            "country": "France",
            "workplace": "Paris",
            "service": "Cardiologie",
            "seller_id": UUID_SELLER_1,
            "state_flag": StateOrderEnum.EXPIRED.value,
            "sending_date": 1666870958,
            "order_accepted_date": 1666870958,
            "demo_flag": True,
            "sharing_authorization": True,
            "company_only": False,
        },
    ]

    response = await client.delete(
        f"/orders/{UUID_ORDER_NOT_FOUND}",
        headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.delete(
        f"/orders/{UUID_ORDER_1}", headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.delete(
        f"/orders/{UUID_ORDER_2}", headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.delete(
        f"/orders/{UUID_ORDER_3}", headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}


@pytest.mark.asyncio
async def test_delete_one_order_from_unknown_user_forbidden(
    client: AsyncClient, session: AsyncSession
) -> None:
    await pre_fill_db(session)
    response = await client.delete(
        f"/orders/{UUID_ORDER_NOT_FOUND}",
        headers={"X-USERINFO": ACCESS_TOKEN_UNKNOWN_USER},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.delete(
        f"/orders/{UUID_ORDER_1}", headers={"X-USERINFO": ACCESS_TOKEN_UNKNOWN_USER}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.delete(
        f"/orders/{UUID_ORDER_2}", headers={"X-USERINFO": ACCESS_TOKEN_UNKNOWN_USER}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.delete(
        f"/orders/{UUID_ORDER_3}", headers={"X-USERINFO": ACCESS_TOKEN_UNKNOWN_USER}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.delete(
        f"/orders/{UUID_ORDER_4}", headers={"X-USERINFO": ACCESS_TOKEN_UNKNOWN_USER}
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

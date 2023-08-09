from httpx import AsyncClient
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv
from typing import Sequence
from moviematchr.services.orders import get_orders_from_local_admin_dal
from moviematchr.schemas.orders.orders import Orders

from tests.conftest import (
    UUID_LOCAL_ADMIN,
    ACCESS_TOKEN_ADMIN,
    ACCESS_TOKEN_LOCAL_ADMIN,
    pre_fill_db,
)

load_dotenv()


@pytest.mark.asyncio
async def test_post_order_from_admin(
    client: AsyncClient, session: AsyncSession
) -> None:
    await pre_fill_db(session)
    response = await client.get(
        "/orders",
        headers={"X-USERINFO": ACCESS_TOKEN_ADMIN},
    )
    assert response.status_code == 200
    orders = response.json()

    response = await client.post(
        "/orders",
        headers={"X-USERINFO": ACCESS_TOKEN_ADMIN},
        json={
            "demo_flag": 0,
            "company_only": False,
            "order_id": "#00000000005",
            "sharing_authorization": True,
            "billing_type": 0,
            "local_admin_email": "samuel.jean@crm.microport.com",
            "local_admin_firstname": "Samuel",
            "local_admin_lastname": "Jean",
            "country": "France",
            "workplace": "New",
            "service": "New",
            "users": [],
            "seller_email": "seller1@gmail.com",
            "seller_firstname": "Seller1FirstName",
            "seller_lastname": "Seller1LastName",
            "seller_phone": "",
        },
    )
    assert response.status_code == 201
    orders.append(response.json())

    response = await client.get(
        "/orders",
        headers={"X-USERINFO": ACCESS_TOKEN_ADMIN},
    )
    assert response.status_code == 200
    assert sorted(response.json(), key=lambda d: d['id'])  == sorted(orders, key=lambda d: d['id'])


@pytest.mark.asyncio
async def test_post_order_from_local_admin(
    client: AsyncClient, session: AsyncSession
) -> None:
    await pre_fill_db(session)
    response = await client.get(
        "/orders",
        headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN},
    )
    orders = response.json()

    response = await client.post(
        "/orders",
        headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN},
        json={
            "demo_flag": 0,
            "company_only": False,
            "order_id": "#00000000005",
            "sharing_authorization": True,
            "billing_type": 0,
            "local_admin_email": "samuel.jean@crm.microport.com",
            "local_admin_firstname": "Samuel",
            "local_admin_lastname": "Jean",
            "country": "France",
            "workplace": "New",
            "service": "New",
            "users": [],
            "seller_email": "seller1@gmail.com",
            "seller_firstname": "Seller1FirstName",
            "seller_lastname": "Seller1LastName",
            "seller_phone": "",
        },
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Forbidden"}

    response = await client.get(
        "/orders",
        headers={"X-USERINFO": ACCESS_TOKEN_LOCAL_ADMIN},
    )
    assert response.status_code == 200
    assert sorted(response.json(), key=lambda d: d['id'])  == sorted(orders, key=lambda d: d['id'])

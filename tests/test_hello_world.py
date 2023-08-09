import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_hello_world1(client: AsyncClient) -> None:
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}

@pytest.mark.asyncio
async def test_hello_world2(client: AsyncClient) -> None:
    #await pre_fill_db(session)
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}

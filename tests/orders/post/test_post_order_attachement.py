import os
from fastapi import HTTPException, Request, File, UploadFile, Response
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from dotenv import load_dotenv
import pytest

from tests.conftest import (
    ACCESS_TOKEN_ADMIN,
    ACCESS_TOKEN_LOCAL_ADMIN,
    ACCESS_TOKEN_MICROPORT_STAFF,
    UUID_LOCAL_ADMIN,
    UUID_ORDER_1,
    pre_fill_db,
)

load_dotenv()

PATH_RESSOURCES_TEST = os.getenv("PATH_RESSOURCES_TEST")

"""
@pytest.mark.asyncio
async def test_post_order_attachement_from_admin2(client: AsyncClient, session: AsyncSession) -> None:
    await pre_fill_db(session)

    filename = "upload_order.xlsx"
    file_path = PATH_RESSOURCES_TEST + "/" + filename

    with open(file_path, "rb") as file:
        upload_file = UploadFile(file)

        response = await client.post(
                f"/orders/{UUID_ORDER_1}/upload",
                headers={
                "X-USERINFO": ACCESS_TOKEN_ADMIN,
                    "Content-Type": "multipart/form-data",
                    "Content-Disposition": f'form-data; name="file"; filename="{upload_file.filename}"',
                },
                data=upload_file.file.read(),
                json={
                    "file": upload_file.file.read(),
                }
            )

        assert response.status_code == 200

@pytest.mark.asyncio
async def test_post_order_attachement_from_admin(client: AsyncClient, session: AsyncSession) -> None:
    await pre_fill_db(session)

    filename = "upload_order.xlsx"
    file_path = PATH_RESSOURCES_TEST + "/" + filename

    with open(file_path, "rb") as file:
      upload_file = file.read()

    response = await client.post(
            f"/orders/{UUID_ORDER_1}/upload",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN},
            json={
                "file": upload_file,
            }
        )
    assert response.status_code == 201
    assert os.path.exists(f"{PATH_ORDERS_UPLOAD}/{UUID_ORDER_1}/#0000000001")

@pytest.mark.asyncio
async def test_post_order_attachement_from_microport_staff(client: AsyncClient, session: AsyncSession) -> None:
    await pre_fill_db(session)

    filename = "upload_order.xlsx"
    project_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(project_dir, filename)

    with open(file_path, "rb") as file:
      file = UploadFile(file, filename="#0000000001")

    response = await client.post(
            f"/orders/{UUID_ORDER_1}/upload",
            headers={"X-USERINFO": ACCESS_TOKEN_MICROPORT_STAFF},
            json={
                "file": file,
            }
        )
    assert response.status_code == 201
    assert os.path.exists(f"{PATH_ORDERS_UPLOAD}/{UUID_ORDER_1}/#0000000001")


@pytest.mark.asyncio
async def test_post_order_attachement_from_local_admin(client: AsyncClient, session: AsyncSession) -> None:
    await pre_fill_db(session)

    filename = "upload_order.xlsx"
    project_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(project_dir, filename)

    with open(file_path, "rb") as file:
      file = UploadFile(file, filename="#0000000001")

    response = await client.post(
            f"/orders/{UUID_ORDER_1}/upload",
            headers={"X-USERINFO": ACCESS_TOKEN_ADMIN},
            json={
                "file": file,
            }
        )
    assert response.status_code == 403
    assert not os.path.exists(f"{PATH_ORDERS_UPLOAD}/{UUID_ORDER_1}/#0000000001")
"""
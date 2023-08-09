import os
import asyncio
import uuid
from httpx import AsyncClient

import pytest
import pytest_asyncio
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from adminplatform.init_base import Base
from adminplatform import app

from adminplatform.schemas.tickets.tickets import Tickets, StateTicketEnum, TypeTicketEnum
from adminplatform.schemas.orders.orders import Orders, StateOrderEnum
from adminplatform.schemas.sellers.sellers import Sellers
from adminplatform.schemas.licences.licences import Licences, TypeLicenceEnum
from adminplatform.schemas.account.user import Type2FA

from adminplatform.services.tickets import create_ticket_dal
from adminplatform.services.orders import create_order_dal
from adminplatform.services.sellers import create_seller_dal
from adminplatform.services.licences import create_licence_dal

from adminplatform.utils.utils import init_bdd

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DB_TEST_URI")

async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)

@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="function")
async def session() -> AsyncSession:
    new_session = sessionmaker(
        async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with new_session() as s:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield s

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await async_engine.dispose()

@pytest_asyncio.fixture
async def client(session):
    def override_init_bdd():
        yield session
        
    app.dependency_overrides[init_bdd] = override_init_bdd

    async with AsyncClient(app=app, base_url='http://localhost:8080') as client:
       yield client

@pytest.fixture
def anyio_backend():
    return "asyncio"

# --- ACCESS TOKENS (KEYCLOAK) --- #
ACCESS_TOKEN_ADMIN = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJJOWlMdzFhWldvRzQxVUt0aTBiaTRRNnZvSHVjdE1fU0FUYkFGZDdpWHp3In0.eyJleHAiOjE2ODgxMzU2NDIsImlhdCI6MTY4ODEzNTM0MiwianRpIjoiMDEwOGM0OGYtNjQzMi00NTM1LTk1ZGYtMWM4M2EwYjhkMTllIiwiaXNzIjoiaHR0cHM6Ly9hdXRoLnBoeXNpby1zZW5zZS5mci9yZWFsbXMvbWFzdGVyIiwiYXVkIjpbInN5bmVzY29wZS1lYXN5LXdlYiIsImFjY291bnQiXSwic3ViIjoiZjdiMDRkYjItYzJjMC00ZDJjLThmNjktMTEwYzhiMTVmNjFlIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoic3luZXNjb3BlLWVhc3ktd2ViIiwibm9uY2UiOiIyYjM0MjliMy1iNWQzLTRkYTEtYjA5Ny03YzNiNjQ2OTdjMDUiLCJzZXNzaW9uX3N0YXRlIjoiYzg0MmQxM2UtOTVmOS00Mjk4LTg3M2UtMDUzMjIwZTdiZjdiIiwiYWNyIjoiMCIsImFsbG93ZWQtb3JpZ2lucyI6WyJodHRwczovL2Rldi5zeW5lc2NvcGUucGh5c2lvLXNlbnNlLmZyIiwiaHR0cHM6Ly9zeW5lc2NvcGUucGh5c2lvLXNlbnNlLmZyIiwiaHR0cDovL2xvY2FsaG9zdDozMDAwIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJkZWZhdWx0LXJvbGVzLW1hc3RlciIsIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBhdWQtc3luZXNjb3BlIHByb2ZpbGUgZW1haWwiLCJzaWQiOiJjODQyZDEzZS05NWY5LTQyOTgtODczZS0wNTMyMjBlN2JmN2IiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6IkhEUyBBZG1pbiIsImdyb3VwcyI6WyIvZWFzeXdlYi9yb2xlcy9oZHNfYWRtaW5fbWljcm9wb3J0IiwiL3VzZXJUeXBlL3BoeXNpY2lhbiIsIi9teVJoeXRobS91c2VyIiwiL2Vhc3l3ZWIvdXNlciJdLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJoZHMtYWRtaW4tbWljcm9wb3J0QHRlc3QuY29tIiwiZ2l2ZW5fbmFtZSI6IkhEUyIsImZhbWlseV9uYW1lIjoiQWRtaW4iLCJlbWFpbCI6Imhkcy1hZG1pbi1taWNyb3BvcnRAdGVzdC5jb20ifQ.pWirOAl5QGQHOcuhj-V0gRoF9KhCSLw6EUpCtNmqCoXebumPmU38J9TOgiLAT3lIyP8vY5iPLDoJkUiuowIwxB-rc-39fV3vmnR0fwf7CdguCkEB-J6ESIdqZZwq_uGno_fx4wzL8QmhmmopmtsxsEKCnmesqwvVxssE4fIzA3LGjzujQi9VSlnlmNzEzFq_YlbTt5_rNwulQ8DSQnkV7-onBLptmKrwjsARZ1sL_qljvX1x-2qUc2HZDud_EaIz5tRQbpJybhebqNcL7BULbpD-o7xuDMJARWJf1-rzkU-JU92wrv8jrIS2PT_bV203QRWB4Y-vo_RYZczC9hicCQ"
ACCESS_TOKEN_MICROPORT_STAFF = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJJOWlMdzFhWldvRzQxVUt0aTBiaTRRNnZvSHVjdE1fU0FUYkFGZDdpWHp3In0.eyJleHAiOjE2ODgxMzU3ODQsImlhdCI6MTY4ODEzNTQ4NCwianRpIjoiZDJjOGUzNTktYTk4OC00ZTgzLTg5ZmYtODFmZmExZTAwNzAyIiwiaXNzIjoiaHR0cHM6Ly9hdXRoLnBoeXNpby1zZW5zZS5mci9yZWFsbXMvbWFzdGVyIiwiYXVkIjpbInN5bmVzY29wZS1lYXN5LXdlYiIsImFjY291bnQiXSwic3ViIjoiY2VkN2Y4NWEtYzMxYS00YmRlLTk0ZTYtZGJjNDU2ZWRiZmFhIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoic3luZXNjb3BlLWVhc3ktd2ViIiwibm9uY2UiOiJjMTc4OGJmMS0wNDg4LTQ3ZTQtYWIzOC1mNmQ4ZDlmZWJlNzMiLCJzZXNzaW9uX3N0YXRlIjoiMTdkYzAzOGYtNjRkMi00OGY3LWFkYTktMThkOTRjZjJkMTYzIiwiYWNyIjoiMCIsImFsbG93ZWQtb3JpZ2lucyI6WyJodHRwczovL2Rldi5zeW5lc2NvcGUucGh5c2lvLXNlbnNlLmZyIiwiaHR0cHM6Ly9zeW5lc2NvcGUucGh5c2lvLXNlbnNlLmZyIiwiaHR0cDovL2xvY2FsaG9zdDozMDAwIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJkZWZhdWx0LXJvbGVzLW1hc3RlciIsIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBhdWQtc3luZXNjb3BlIHByb2ZpbGUgZW1haWwiLCJzaWQiOiIxN2RjMDM4Zi02NGQyLTQ4ZjctYWRhOS0xOGQ5NGNmMmQxNjMiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6Ik1pY3JvcG9ydC1zdGFmZiBUZXN0IiwiZ3JvdXBzIjpbIi9lYXN5d2ViL3JvbGVzL2xvY2FsX2FkbWluIiwiL2Vhc3l3ZWIvcm9sZXMvbWljcm9wb3J0X3N0YWZmIiwiL3VzZXJUeXBlL3BoeXNpY2lhbiIsIi9teVJoeXRobS91c2VyIiwiL2Vhc3l3ZWIvdXNlciJdLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJtaWNyb3BvcnQtc3RhZmZAdGVzdC5jb20iLCJnaXZlbl9uYW1lIjoiTWljcm9wb3J0LXN0YWZmIiwiZmFtaWx5X25hbWUiOiJUZXN0IiwiZW1haWwiOiJtaWNyb3BvcnQtc3RhZmZAdGVzdC5jb20ifQ.KZ4bHfQ-jjBn8sokHrmy8zhSNbQ4KlYYqeHQVQmuM4LcgF3PLpPy3PCPKAzX__dy76l1GXZYRy7TWy9fXv73kPYJ2xxWjWIs4s0RirfxcDIKUOza6ImwpO0_mjogPQ7Vfg4n0na9TZnvoaWnohBIAMpqun60EpXsSHe0bFRtgZqXnZAo6_OuIwilvJ0ww3IG3R_LARKb9_Zc9gq24FoIcyhnHJeX3MAtOkwYv_JeydX0Rv2Hc2nqXYnOmI4Nmt85lR5DaqaNTBDPAofHRTsZ9FCbobpOWHZcdACFguUnRZZrdQAfObE6SrOnCMD_NHrzsQbb6eoyNnNHTwQNQypH6A"
ACCESS_TOKEN_LOCAL_ADMIN = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJJOWlMdzFhWldvRzQxVUt0aTBiaTRRNnZvSHVjdE1fU0FUYkFGZDdpWHp3In0.eyJleHAiOjE2ODgxMzYwMjEsImlhdCI6MTY4ODEzNTcyMSwianRpIjoiMTIzNjcyMjYtMTliOC00NWU0LWFmYjAtZDYxYzNmZWRiNzMyIiwiaXNzIjoiaHR0cHM6Ly9hdXRoLnBoeXNpby1zZW5zZS5mci9yZWFsbXMvbWFzdGVyIiwiYXVkIjpbInN5bmVzY29wZS1lYXN5LXdlYiIsImFjY291bnQiXSwic3ViIjoiOWUzM2E4YTEtNjE1ZC00OGY4LTg0MTYtYzRmNTIzY2IwNWE3IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoic3luZXNjb3BlLWVhc3ktd2ViIiwibm9uY2UiOiJlODI4NDQyNi1kNTdjLTQxZmYtOWIxMC0xMjJiOWQwYWEyNjQiLCJzZXNzaW9uX3N0YXRlIjoiYWZiNTllYjMtNjBlYy00YmQ5LWIyNmYtZjgwMWVmOGEwYjFmIiwiYWNyIjoiMCIsImFsbG93ZWQtb3JpZ2lucyI6WyJodHRwczovL2Rldi5zeW5lc2NvcGUucGh5c2lvLXNlbnNlLmZyIiwiaHR0cHM6Ly9zeW5lc2NvcGUucGh5c2lvLXNlbnNlLmZyIiwiaHR0cDovL2xvY2FsaG9zdDozMDAwIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJkZWZhdWx0LXJvbGVzLW1hc3RlciIsIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6Im9wZW5pZCBhdWQtc3luZXNjb3BlIHByb2ZpbGUgZW1haWwiLCJzaWQiOiJhZmI1OWViMy02MGVjLTRiZDktYjI2Zi1mODAxZWY4YTBiMWYiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZ3JvdXBzIjpbIi9lYXN5d2ViL3JvbGVzL2xvY2FsX2FkbWluIiwiL3VzZXJUeXBlL3BoeXNpY2lhbiIsIi9teVJoeXRobS91c2VyIl0sInByZWZlcnJlZF91c2VybmFtZSI6ImxvY2FsLWFkbWluQHRlc3QuY29tIiwiZ2l2ZW5fbmFtZSI6IiIsImZhbWlseV9uYW1lIjoiIiwiZW1haWwiOiJsb2NhbC1hZG1pbkB0ZXN0LmNvbSJ9.IHOg0o86jRyAyDEiK24TQUcsFyidty75zRGXWXGcr_ieKWB31wlEbhSOlVCvtfq4n0tHP46IdgMoCfWxpOC-HI5ggak7nGYSOhW9VDWKXcvONiaDbvN028BLMrPamAf2RgKwueNdALeABSwHLTbk7zCm_-kx_cAVIvf7Ch0zr5vOyf7DecfbgBuSg-W13n6kPtE7A3ObbuLjdrkEnLlDl4gu1y36TazQ1hVKxPF56hXsG4A2lssFtyDeEJqMjv4i7mAddRo-dF7lrbAcs9SMz9GhvNiX20rMUu0JHBXhxttaNoMyIaLf1FobucAN_tIBpicQocuD92Osn6xqluFdNA"
ACCESS_TOKEN_UNKNOWN_USER = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJJOWlMdzFhWldvRzQxVUt0aTBiaTRRNnZvSHVjdE1fU0FUYkFGZDdpWHp3In0.eyJleHAiOjE2NzY1NTkyNjAsImlhdCI6MTY3NjU1ODk2MCwiYXV0aF90aW1lIjoxNjc2NTU4OTU4LCJqdGkiOiJhODFiNDUzNC05MzlkLTQ2NDMtODRlZC0yN2I3OTc1Njk1YzAiLCJpc3MiOiJodHRwczovL2F1dGgucGh5c2lvLXNlbnNlLmZyL3JlYWxtcy9tYXN0ZXIiLCJhdWQiOlsic3luZXNjb3BlLWVhc3ktd2ViIiwiYWNjb3VudCJdLCJzdWIiOiIzMDEyN2I5Zi0yZGQ5LTQ3NzEtYjA0MC05MWE0ZjNjMzU5YzAiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJzeW5lc2NvcGUtZWFzeS13ZWIiLCJub25jZSI6Ijc2OWJmOTQxLTg2OGMtNGUwMi04NWNjLWM5MzZhNTg0MDA0NyIsInNlc3Npb25fc3RhdGUiOiI5M2U2YzllMS01ODFmLTQzOTgtYWRiNi01OWVlMTU1NWE3YjMiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbImh0dHBzOi8vc3luZXNjb3BlLnBoeXNpby1zZW5zZS5mciIsImh0dHA6Ly9sb2NhbGhvc3Q6MzAwMCJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1tYXN0ZXIiLCJvZmZsaW5lX2FjY2VzcyIsInVtYV9hdXRob3JpemF0aW9uIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgYXVkLXN5bmVzY29wZSBwcm9maWxlIGVtYWlsIiwic2lkIjoiOTNlNmM5ZTEtNTgxZi00Mzk4LWFkYjYtNTllZTE1NTVhN2IzIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm5hbWUiOiJOb24tbWVkaWNhbC1zdGFmZiBUZXN0IiwiZ3JvdXBzIjpbIi9lYXN5d2ViL3JvbGVzL25vbl9tZWRpY2FsX3N0YWZmIiwiL3VzZXJUeXBlL3BoeXNpY2lhbiIsIi9teVJoeXRobS91c2VyIiwiL2Vhc3l3ZWIvdXNlciJdLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJub24tbWVkaWNhbC1zdGFmZkB0ZXN0LmNvbSIsImdpdmVuX25hbWUiOiJOb24tbWVkaWNhbC1zdGFmZiIsImZhbWlseV9uYW1lIjoiVGVzdCIsImVtYWlsIjoibm9uLW1lZGljYWwtc3RhZmZAdGVzdC5jb20ifQ.VqG1OBGZyYOJD-WVpTcyPfqPmR_QRUdtUlSWx0l3KhaeA10G9qeX-IqTrtmYGSbY8WCPqce_JB8lshKGA2wqdg8g2TellJ1-G_9LEHb3RQM6HA6WtmNNPBeVkzMzUF2Nw6xjX-hHL5c3fwQLaVD6iVp_ayFExH7BzA1d2SY_6vk2N-Xj7leqE5FSP4e6PYh7siaCZOkHf4WxHot8FtvoDv2qpi8ColnoeE9VDF2Wn3KB8sysE4WNPw2YIAbTs2l1cBSLtF0vkl99cX5BIx6Ggnd4hSOdvC61jYY6t9RBcXLVNvNr0vxRr-_kkmy9QHlBeXAlno6p5sT99oz7kFKoJA"

# --- ID USER (KEYCLOAK) --- #
UUID_ADMIN = "f7b04db2-c2c0-4d2c-8f69-110c8b15f61e"
UUID_MICROPORT_STAFF = "ced7f85a-c31a-4bde-94e6-dbc456edbfaa"
UUID_LOCAL_ADMIN = "9e33a8a1-615d-48f8-8416-c4f523cb05a7"

# --- ID SELLER (DB) --- #
UUID_SELLER_NOT_FOUND = "e227d564-3238-473c-aff7-630bdcd6cfc0"
UUID_SELLER_1 = "e227d564-3238-473c-aff7-630bdcd6cfc1"
UUID_SELLER_2 = "e227d564-3238-473c-aff7-630bdcd6cfc2"
UUID_SELLER_3 = "e227d564-3238-473c-aff7-630bdcd6cfc3"
UUID_SELLER_4 = "e227d564-3238-473c-aff7-630bdcd6cfc4"

# --- ID ORDER (DB) --- #
UUID_ORDER_NOT_FOUND = "e227d564-3238-473c-aff7-630bdcd6cfb0"
UUID_ORDER_1 = "e227d564-3238-473c-aff7-630bdcd6cfb1"
UUID_ORDER_2 = "e227d564-3238-473c-aff7-630bdcd6cfb2"
UUID_ORDER_3 = "e227d564-3238-473c-aff7-630bdcd6cfb3"
UUID_ORDER_4 = "e227d564-3238-473c-aff7-630bdcd6cfb4"

# --- ID LICENCE (DB) --- #
UUID_LICENCE_1 = "e227d564-3238-473c-aff7-630bdcd6cfd1"
UUID_LICENCE_2 = "e227d564-3238-473c-aff7-630bdcd6cfd2"
UUID_LICENCE_3 = "e227d564-3238-473c-aff7-630bdcd6cfd3"
UUID_LICENCE_4 = "e227d564-3238-473c-aff7-630bdcd6cfd4"
UUID_LICENCE_5 = "e227d564-3238-473c-aff7-630bdcd6cfd5"
UUID_LICENCE_6 = "e227d564-3238-473c-aff7-630bdcd6cfd6"

# --- SERIAL NUMBER LICENCE (DB) --- #
SERIAL_LICENCE_1 = "YB2304063E"
SERIAL_LICENCE_2 = "YB2304064E"
SERIAL_LICENCE_3 = "YB2304065E"
SERIAL_LICENCE_4 = "YB2304066E"
SERIAL_LICENCE_5 = "YB2304067E"
SERIAL_LICENCE_6 = "YB2304068E"

# --- UNUSED ID LICENCE (DB) --- #*
UNUSED_UUID_LICENCE_1 = "e227d564-3238-473c-aff7-630bdcd6cfe1"
UNUSED_UUID_LICENCE_2 = "e227d564-3238-473c-aff7-630bdcd6cfe2"
UNUSED_UUID_LICENCE_3 = "e227d564-3238-473c-aff7-630bdcd6cfe3"
UNUSED_UUID_LICENCE_4 = "e227d564-3238-473c-aff7-630bdcd6cfe4"
UNUSED_UUID_LICENCE_5 = "e227d564-3238-473c-aff7-630bdcd6cfe5"
UNUSED_UUID_LICENCE_6 = "e227d564-3238-473c-aff7-630bdcd6cfe6"
UNUSED_UUID_LICENCE_7 = "e227d564-3238-473c-aff7-630bdcd6cfe7"
UNUSED_UUID_LICENCE_8 = "e227d564-3238-473c-aff7-630bdcd6cfe8"
UNUSED_UUID_LICENCE_9 = "e227d564-3238-473c-aff7-630bdcd6cfe9"
UNUSED_UUID_LICENCE_10 = "e227d564-3238-473c-aff7-630bdcd6cfea"
UNUSED_UUID_LICENCE_11 = "e227d564-3238-473c-aff7-630bdcd6cfeb"
UNUSED_UUID_LICENCE_12 = "e227d564-3238-473c-aff7-630bdcd6cfec"
UNUSED_UUID_LICENCE_13 = "e227d564-3238-473c-aff7-630bdcd6cfed"

# --- UNUSED SERIAL NUMBER LICENCE (DB) --- #
UNUSED_SERIAL_LICENCE_1 = "YB2304001Z"
UNUSED_SERIAL_LICENCE_2 = "YB2304002Z"
UNUSED_SERIAL_LICENCE_3 = "YB2304003Z"
UNUSED_SERIAL_LICENCE_4 = "YB2304004Z"
UNUSED_SERIAL_LICENCE_5 = "YB2304005Z"
UNUSED_SERIAL_LICENCE_6 = "YB2304006Z"
UNUSED_SERIAL_LICENCE_7 = "YB2304007Z"
UNUSED_SERIAL_LICENCE_8 = "YB2304008Z"
UNUSED_SERIAL_LICENCE_9 = "YB2304009Z"
UNUSED_SERIAL_LICENCE_10 = "YB2304010Z"
UNUSED_SERIAL_LICENCE_11 = "YB2304011Z"
UNUSED_SERIAL_LICENCE_12 = "YB2304012Z"
UNUSED_SERIAL_LICENCE_13 = "YB2304013Z"

# --- ID USER LICENCE (DB & KEYCLOAK) --- #
USER_LICENCE_ID_1 = "af3bf726-afc4-4ce1-bd99-3f915056b1da"
USER_LICENCE_ID_2 = "bee69746-70f8-4aaf-9784-674480ecbdad"
USER_LICENCE_ID_3 = "e864c16d-55c8-4371-8867-30c95e5d82cc"
USER_LICENCE_ID_4 = "7ce2ebdf-8ff1-470e-ad1d-fc0c89fdc6fa"
USER_LICENCE_ID_5 = "6d9b3c07-f0b8-42d8-acaa-2c322cf30f89"
USER_LICENCE_ID_6 = "3e2b8a58-7f52-45f1-b5a0-5b84eea05777"

# --- ID TICKET (DB) --- #
UUID_TICKET_NOT_FOUND = "e227d564-3238-473c-aff7-630bdcd6cfa0"
UUID_TICKET_1 = "e227d564-3238-473c-aff7-630bdcd6cfa1"
UUID_TICKET_2 = "e227d564-3238-473c-aff7-630bdcd6cfa2"
UUID_TICKET_3 = "e227d564-3238-473c-aff7-630bdcd6cfa3"
UUID_TICKET_4 = "e227d564-3238-473c-aff7-630bdcd6cfa4"
UUID_TICKET_5 = "e227d564-3238-473c-aff7-630bdcd6cfa5"
UUID_TICKET_6 = "e227d564-3238-473c-aff7-630bdcd6cfa6"

async def pre_fill_db(db: AsyncSession):
    await create_seller_dal(
        db,
        Sellers(
            id=UUID_SELLER_1,
            email="seller1@gmail.com",
            firstname="Seller1FirstName",
            lastname="Seller1LastName",
        ),
    )

    await create_seller_dal(
        db,
        Sellers(
            id=UUID_SELLER_2,
            email="seller2@gmail.com",
            firstname="Seller2FirstName",
            lastname="Seller2LastName",
        ),
    )

    await create_seller_dal(
        db,
        Sellers(
            id=UUID_SELLER_3,
            email="seller3@gmail.com",
            firstname="Seller3FirstName",
            lastname="Seller3LastName",
        ),
    )

    await create_seller_dal(
        db,
        Sellers(
            id=UUID_SELLER_4,
            email="seller4@gmail.com",
            firstname="Seller4FirstName",
            lastname="Seller4LastName",
        ),
    )

    # --- ORDER 1 : #0000000001 --- #
    await create_order_dal(
        db,
        Orders(
            id=UUID_ORDER_1,
            order_id="#0000000001",
            local_admin_id=UUID_LOCAL_ADMIN,
            country="France",
            workplace="Gotham",
            service="Cardiologie",
            seller_id=UUID_SELLER_1,
            state_flag=StateOrderEnum.ACCEPTED.value,
            sending_date=1666870958,
            order_accepted_date=1666870958,
            demo_flag=False,
        )
    )

    await create_licence_dal(
        db,
        Licences(
            id=UUID_LICENCE_1,
            licence_type=TypeLicenceEnum.DOCTOR.value,
            serial_number=SERIAL_LICENCE_1,
            id_order=UUID_ORDER_1,
            id_user=USER_LICENCE_ID_1,
            demo_flag=False,
            active=True,
        ),
    )

    await create_licence_dal(
        db,
        Licences(
            id=UUID_LICENCE_2,
            licence_type=TypeLicenceEnum.DOCTOR.value,
            serial_number=SERIAL_LICENCE_2,
            id_order=UUID_ORDER_1,
            id_user=USER_LICENCE_ID_2,
            demo_flag=False,
            active=True,
        ),
    )

    await create_licence_dal(
        db,
        Licences(
            id=UUID_LICENCE_4,
            licence_type=TypeLicenceEnum.MEDICAL_STAFF.value,
            serial_number=SERIAL_LICENCE_4,
            id_order=UUID_ORDER_1,
            id_user=USER_LICENCE_ID_4,
            demo_flag=False,
            active=True,
        ),
    )

    await create_licence_dal(
        db,
        Licences(
            id=UNUSED_UUID_LICENCE_1,
            licence_type=None,
            serial_number=UNUSED_SERIAL_LICENCE_1,
            id_order=UUID_ORDER_1,
            id_user=None,
            nb_recording_analyzed=0,
            demo_flag=False,
            active=True,
        )
    )
    
    await create_licence_dal(
        db,
        Licences(
            id=UNUSED_UUID_LICENCE_2,
            licence_type=None,
            serial_number=UNUSED_SERIAL_LICENCE_2,
            id_order=UUID_ORDER_1,
            id_user=None,
            nb_recording_analyzed=0,
            demo_flag=False,
            active=True,
        )
    )

    await create_licence_dal(
        db,
        Licences(
            id=UNUSED_UUID_LICENCE_3,
            licence_type=None,
            serial_number=UNUSED_SERIAL_LICENCE_3,
            id_order=UUID_ORDER_1,
            id_user=None,
            nb_recording_analyzed=0,
            demo_flag=False,
            active=True,
        )
    )

    await create_licence_dal(
        db,
        Licences(
            id=UNUSED_UUID_LICENCE_4,
            licence_type=None,
            serial_number=UNUSED_SERIAL_LICENCE_4,
            id_order=UUID_ORDER_1,
            id_user=None,
            nb_recording_analyzed=0,
            demo_flag=False,
            active=True,
        )
    )

    await create_licence_dal(
        db,
        Licences(
            id=UNUSED_UUID_LICENCE_5,
            licence_type=None,
            serial_number=UNUSED_SERIAL_LICENCE_5,
            id_order=UUID_ORDER_1,
            id_user=None,
            nb_recording_analyzed=0,
            demo_flag=False,
            active=True,
        )
    )

    # --- ORDER 2 : #0000000002 --- #
    await create_order_dal(
        db,
        Orders(
            id=UUID_ORDER_2,
            order_id="#0000000002",
            local_admin_id=UUID_LOCAL_ADMIN,
            country="France",
            workplace="La Rochelle",
            service="Cardiologie",
            seller_id=UUID_SELLER_1,
            state_flag=StateOrderEnum.ACCEPTED.value,
            sending_date=1666870958,
            order_accepted_date=1666870958,
            demo_flag=False,
        )
    )

    await create_licence_dal(
        db,
        Licences(
            id=UUID_LICENCE_3,
            licence_type=TypeLicenceEnum.DOCTOR.value,
            serial_number=SERIAL_LICENCE_3,
            id_order=UUID_ORDER_2,
            id_user=USER_LICENCE_ID_3,
            demo_flag=False,
            active=True,
        ),
    )

    await create_licence_dal(
        db,
        Licences(
            id=UUID_LICENCE_5,
            licence_type=TypeLicenceEnum.MEDICAL_STAFF.value,
            serial_number=SERIAL_LICENCE_5,
            id_order=UUID_ORDER_2,
            id_user=USER_LICENCE_ID_5,
            demo_flag=False,
            active=True,
        ),
    )

    await create_licence_dal(
        db,
        Licences(
            id=UUID_LICENCE_6,
            licence_type=TypeLicenceEnum.MEDICAL_STAFF.value,
            serial_number=SERIAL_LICENCE_6,
            id_order=UUID_ORDER_2,
            id_user=USER_LICENCE_ID_6,
            demo_flag=False,
            active=True,
        ),
    )

    await create_licence_dal(
        db,
        Licences(
            id=UNUSED_UUID_LICENCE_6,
            licence_type=None,
            serial_number=UNUSED_SERIAL_LICENCE_6,
            id_order=UUID_ORDER_2,
            id_user=None,
            nb_recording_analyzed=0,
            demo_flag=False,
            active=True,
        )
    )

    await create_licence_dal(
        db,
        Licences(
            id=UNUSED_UUID_LICENCE_7,
            licence_type=None,
            serial_number=UNUSED_SERIAL_LICENCE_7,
            id_order=UUID_ORDER_2,
            id_user=None,
            nb_recording_analyzed=0,
            demo_flag=False,
            active=True,
        )
    )

    await create_licence_dal(
        db,
        Licences(
            id=UNUSED_UUID_LICENCE_8,
            licence_type=None,
            serial_number=UNUSED_SERIAL_LICENCE_8,
            id_order=UUID_ORDER_2,
            id_user=None,
            nb_recording_analyzed=0,
            demo_flag=False,
            active=True,
        )
    )

    # --- ORDER 3 : #0000000003 --- #
    await create_order_dal(
        db,
        Orders(
            id=UUID_ORDER_3,
            order_id="#0000000003",
            local_admin_id=UUID_ADMIN,
            country="France",
            workplace="Royan",
            service="Cardiologie",
            seller_id=UUID_SELLER_1,
            state_flag=StateOrderEnum.ACCEPTED.value,
            sending_date=1666870958,
            order_accepted_date=1666870958,
            demo_flag=False,
        )
    )

    await create_licence_dal(
        db,
        Licences(
            id=UNUSED_UUID_LICENCE_9,
            licence_type=None,
            serial_number=UNUSED_SERIAL_LICENCE_9,
            id_order=UUID_ORDER_3,
            id_user=None,
            nb_recording_analyzed=0,
            demo_flag=False,
            active=True,
        )
    )

    await create_licence_dal(
        db,
        Licences(
            id=UNUSED_UUID_LICENCE_10,
            licence_type=None,
            serial_number=UNUSED_SERIAL_LICENCE_10,
            id_order=UUID_ORDER_3,
            id_user=None,
            nb_recording_analyzed=0,
            demo_flag=False,
            active=True,
        )
    )

    # --- ORDER 4 : #0000000004 --- #
    await create_order_dal(
        db,
        Orders(
            id=UUID_ORDER_4,
            order_id="#0000000004",
            local_admin_id=UUID_LOCAL_ADMIN,
            country="France",
            workplace="Paris",
            service="Cardiologie",
            seller_id=UUID_SELLER_1,
            state_flag=StateOrderEnum.EXPIRED.value,
            sending_date=1666870958,
            order_accepted_date=1666870958,
            demo_flag=True,
        )
    )

    await create_licence_dal(
        db,
        Licences(
            id=UNUSED_UUID_LICENCE_11,
            licence_type=None,
            serial_number=UNUSED_SERIAL_LICENCE_11,
            id_order=UUID_ORDER_4,
            id_user=None,
            nb_recording_analyzed=0,
            demo_flag=False,
            active=True,
        )
    )

    await create_licence_dal(
        db,
        Licences(
            id=UNUSED_UUID_LICENCE_12,
            licence_type=None,
            serial_number=UNUSED_SERIAL_LICENCE_12,
            id_order=UUID_ORDER_4,
            id_user=None,
            nb_recording_analyzed=0,
            demo_flag=False,
            active=True,
        )
    )

    await create_licence_dal(
        db,
        Licences(
            id=UNUSED_UUID_LICENCE_13,
            licence_type=None,
            serial_number=UNUSED_SERIAL_LICENCE_13,
            id_order=UUID_ORDER_4,
            id_user=None,
            nb_recording_analyzed=0,
            demo_flag=False,
            active=True,
        )
    )

    await create_ticket_dal(
        db,
        Tickets(
            id=UUID_TICKET_1,
            id_order=UUID_ORDER_1,
            user=UUID_LOCAL_ADMIN,
            type=TypeTicketEnum.MODIFY_USER.value,
            sending_date=1666870958,
            body={
                "type_2fa": Type2FA.EMAIL.value,
                "email": "sjeanpro28@gmail.com",
                "new_email": "sjeanpro28@gmail.com",
                "firstname": "Samuel_Test",
                "lastname": "Jean_Test",
            },
            state_flag=StateTicketEnum.IN_PROGRESS.value,
            update_state_date=None,
        ),
    )

    await create_ticket_dal(
        db,
        Tickets(
            id=UUID_TICKET_2,
            id_order=UUID_ORDER_1,
            user=UUID_ADMIN,
            type=TypeTicketEnum.MODIFY_USER.value,
            sending_date=1666870958,
            body={
                "type_2fa": Type2FA.EMAIL.value,
                "email": "sjeanpro28@gmail.com",
                "new_email": "sjeanpro28@gmail.com",
                "firstname": "Samuel_Test",
                "lastname": "Jean_Test",
            },
            state_flag=StateTicketEnum.IN_PROGRESS.value,
            update_state_date=None,
        ),
    )

    await create_ticket_dal(
        db,
        Tickets(
            id=UUID_TICKET_3,
            id_order=UUID_ORDER_1,
            user=UUID_LOCAL_ADMIN,
            type=TypeTicketEnum.MODIFY_USER.value,
            sending_date=1666870958,
            body={
                "type_2fa": Type2FA.EMAIL.value,
                "email": "sjeanpro28@gmail.com",
                "new_email": "sjeanpro28@gmail.com",
                "firstname": "Samuel_Test",
                "lastname": "Jean_Test",
            },
            state_flag=StateTicketEnum.IN_PROGRESS.value,
            update_state_date=None,
        ),
    )

    await create_ticket_dal(
        db,
        Tickets(
            id=UUID_TICKET_4,
            id_order=UUID_ORDER_1,
            user=UUID_ADMIN,
            type=TypeTicketEnum.MODIFY_USER.value,
            sending_date=1666870958,
            body={
                "type_2fa": Type2FA.EMAIL.value,
                "email": "sjeanpro28@gmail.com",
                "new_email": "sjeanpro28@gmail.com",
                "firstname": "Samuel_Test",
                "lastname": "Jean_Test",
            },
            state_flag=StateTicketEnum.IN_PROGRESS.value,
            update_state_date=None,
        ),
    )

    await db.commit()

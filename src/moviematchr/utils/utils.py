import os

from os.path import exists
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DB_URI")

# SQLACLHEMY SETUP
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)

session_locale = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

NB_SECONDS_IN_A_DAY = 86400


def init_env():
    env_path = Path("..") / ".env"

    if exists(env_path):
        load_dotenv(dotenv_path=env_path)


# Get an instance of database
async def init_bdd():
    db: AsyncSession = session_locale()

    async with db as session:
        try:
            yield session
        finally:
            await session.close()

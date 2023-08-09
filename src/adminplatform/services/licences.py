from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from adminplatform.models.licences import DBLicences
from adminplatform.schemas.licences.licences import Licences


# Methods for interacting with the database
async def get_licence_dal(db: AsyncSession, id: str):
    query = select(DBLicences).where(DBLicences.id == id)
    res = await db.execute(query)
    return res.scalars().first()


async def get_licences_dal(db: AsyncSession):
    query = select(DBLicences)
    res = await db.execute(query)
    return res.scalars().all()

async def get_licences_from_order_dal(db: AsyncSession, id_order: str):
    query = select(DBLicences).where(DBLicences.id_order == id_order)
    res = await db.execute(query)
    return res.scalars().all()

async def get_licence_from_serial_dal(db: AsyncSession, serial: str):
    query = select(DBLicences).where(DBLicences.serial_number == serial)
    res = await db.execute(query)
    return res.scalars().first()

async def create_licence_dal(db: AsyncSession, licence: Licences):
    db_licences = DBLicences(**licence.dict())
    db.add(db_licences)
    await db.flush()
    await db.refresh(db_licences)

    return db_licences


async def delete_licence_dal(db: AsyncSession, id: str):
    query = delete(DBLicences).where(DBLicences.id == id)
    await db.execute(query)
    await db.flush()


async def update_licence_dal(db: AsyncSession, licence: Licences):
    db.add(licence)
    await db.flush()
    await db.refresh(licence)

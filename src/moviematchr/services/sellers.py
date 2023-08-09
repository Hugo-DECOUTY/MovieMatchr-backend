from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from moviematchr.models.sellers import DBSellers
from moviematchr.schemas.sellers.sellers import Sellers


# Methods for interacting with the database
async def get_seller_dal(db: AsyncSession, id: str):
    query = select(DBSellers).where(DBSellers.id == id)
    res = await db.execute(query)
    return res.scalars().first()


async def get_seller_by_email_dal(db: AsyncSession, email: str):
    query = select(DBSellers).where(DBSellers.email == email)
    res = await db.execute(query)
    return res.scalars().first()


async def get_sellers_dal(db: AsyncSession):
    query = select(DBSellers)
    res = await db.execute(query)
    return res.scalars().all()


async def create_seller_dal(db: AsyncSession, seller: Sellers):
    db_sellers = DBSellers(**seller.dict())
    db.add(db_sellers)
    await db.flush()
    await db.refresh(db_sellers)

    return db_sellers


async def delete_seller_dal(db: AsyncSession, id: str, email: str):
    query = delete(DBSellers).where(DBSellers.id == id, DBSellers.email == email)
    await db.execute(query)
    await db.flush()


async def update_seller_dal(db: AsyncSession, seller: Sellers):
    db.add(seller)
    await db.flush()
    await db.refresh(seller)

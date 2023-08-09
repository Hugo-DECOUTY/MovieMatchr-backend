from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from moviematchr.models.transactions import DBTransactions
from moviematchr.schemas.transactions.transactions import Transactions


# Methods for interacting with the database
async def get_transaction_dal(db: AsyncSession, transaction_id: str):
    query = select(DBTransactions).where(DBTransactions.id == transaction_id)
    res = await db.execute(query)
    return res.scalars().first()


async def get_transactions_dal(db: AsyncSession):
    query = select(DBTransactions)
    res = await db.execute(query)
    return res.scalars().all()

async def get_transactions_from_complementary_id_dal(db: AsyncSession, complementary_id: str):
    query = select(DBTransactions).where(DBTransactions.complementary_id == complementary_id)
    res = await db.execute(query)
    return res.scalars().all()

async def get_transactions_from_recording_id_dal(db: AsyncSession, recording_id: str):
    query = select(DBTransactions).where(DBTransactions.recording_id == recording_id)
    res = await db.execute(query)
    return res.scalars().all()

async def create_transaction_dal(db: AsyncSession, transaction: Transactions):
    db_transactions = DBTransactions(**transaction.dict())
    db.add(db_transactions)
    await db.flush()
    await db.refresh(db_transactions)

    return db_transactions


async def delete_transaction_dal(db: AsyncSession, transaction_id: str):
    query = delete(DBTransactions).where(DBTransactions.id == transaction_id)
    await db.execute(query)
    await db.flush()


async def update_transaction_dal(db: AsyncSession, transaction: Transactions):
    db.add(transaction)
    await db.flush()
    await db.refresh(transaction)

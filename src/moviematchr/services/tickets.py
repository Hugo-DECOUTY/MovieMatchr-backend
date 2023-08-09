from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from moviematchr.models.tickets import DBTickets
from moviematchr.schemas.tickets.tickets import Tickets


# Methods for interacting with the database
async def get_ticket_dal(db: AsyncSession, ticket_id: str):
    query = select(DBTickets).where(DBTickets.id == ticket_id)
    res = await db.execute(query)
    return res.scalars().first()


async def get_tickets_dal(db: AsyncSession):
    query = select(DBTickets)
    res = await db.execute(query)
    return res.scalars().all()

async def get_tickets_from_order_dal(db: AsyncSession, id_order: str):
    query = select(DBTickets).where(DBTickets.id_order == id_order)
    res = await db.execute(query)
    return res.scalars().all()


async def get_tickets_order_by_sending_date_dal(db: AsyncSession):
    query = select(DBTickets).order_by(DBTickets.sending_date.desc())
    res = await db.execute(query)
    return res.scalars().all()


async def get_tickets_from_user_dal(db: AsyncSession, user: str):
    query = select(DBTickets).where(DBTickets.user == user)
    res = await db.execute(query)
    return res.scalars().all()

async def get_tickets_from_state_dal(db: AsyncSession, state_flag: int):
    query = select(DBTickets).where(DBTickets.state_flag == state_flag)
    res = await db.execute(query)
    return res.scalars().all()


async def get_tickets_from_user_order_by_hookupday_dal(
    db: AsyncSession, user: str
):
    query = (
        select(DBTickets)
        .where(DBTickets.user == user)
        .order_by(DBTickets.sending_date.desc())
    )
    res = await db.execute(query)
    return res.scalars().all()


async def create_ticket_dal(db: AsyncSession, ticket: Tickets):
    db_tickets = DBTickets(**ticket.dict())
    db.add(db_tickets)
    await db.flush()
    await db.refresh(db_tickets)

    return db_tickets


async def delete_ticket_dal(db: AsyncSession, ticket_id: str):
    query = delete(DBTickets).where(DBTickets.id == ticket_id)
    await db.execute(query)
    await db.flush()


async def update_ticket_dal(db: AsyncSession, ticket: Tickets):
    db.add(ticket)
    await db.flush()
    await db.refresh(ticket)

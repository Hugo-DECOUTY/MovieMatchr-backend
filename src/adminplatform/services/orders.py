from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from adminplatform.models.orders import DBOrders
from adminplatform.schemas.orders.orders import Orders


# Methods for interacting with the database
async def get_order_dal(db: AsyncSession, id: str):
    query = select(DBOrders).where(DBOrders.id == id)
    res = await db.execute(query)
    return res.scalars().first()


async def get_orders_dal(db: AsyncSession):
    query = select(DBOrders)
    res = await db.execute(query)
    return res.scalars().all()


async def get_orders_order_by_sending_date_dal(db: AsyncSession):
    query = select(DBOrders).order_by(DBOrders.sending_date.desc())
    res = await db.execute(query)
    return res.scalars().all()


async def get_orders_from_local_admin_dal(db: AsyncSession, local_admin_id: str):
    query = select(DBOrders).where(DBOrders.local_admin_id == local_admin_id)
    res = await db.execute(query)
    return res.scalars().all()

async def get_orders_from_state_dal(db: AsyncSession, state_flag: int):
    query = select(DBOrders).where(DBOrders.state_flag == state_flag)
    res = await db.execute(query)
    return res.scalars().all()


async def get_orders_from_local_admin_order_by_hookupday_dal(
    db: AsyncSession, local_admin_id: str
):
    query = (
        select(DBOrders)
        .where(DBOrders.local_admin_id == local_admin_id)
        .order_by(DBOrders.sending_date.desc())
    )
    res = await db.execute(query)
    return res.scalars().all()


async def create_order_dal(db: AsyncSession, order: Orders):
    db_orders = DBOrders(**order.dict())
    db.add(db_orders)
    await db.flush()
    await db.refresh(db_orders)

    return db_orders


async def delete_order_dal(db: AsyncSession, id: str):
    query = delete(DBOrders).where(DBOrders.id == id)
    await db.execute(query)
    await db.flush()


async def update_order_dal(db: AsyncSession, order: Orders):
    db.add(order)
    await db.flush()
    await db.refresh(order)

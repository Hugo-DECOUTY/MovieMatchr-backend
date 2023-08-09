from typing import List
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from adminplatform.controller.tickets.create_ticket import create_ticket
from adminplatform.controller.tickets.delete_ticket import delete_ticket
from adminplatform.controller.tickets.get_ticket import get_ticket
from adminplatform.controller.tickets.get_tickets import get_tickets
from adminplatform.controller.tickets.process_ticket import process_ticket
from adminplatform.controller.tickets.update_ticket import update_ticket

from adminplatform.schemas.tickets.info_get_tickets import InfoGetTickets
from adminplatform.schemas.tickets.info_patch_tickets import InfoPatchTickets
from adminplatform.schemas.tickets.info_process_tickets import InfoProcessTickets
from adminplatform.schemas.tickets.info_post_tickets import InfoPostTickets
from adminplatform.schemas.tickets.tickets import Tickets

from adminplatform.utils.utils import init_bdd

router = APIRouter()

# Routes for interacting with the API
# --------------- POST ---------------
@router.post("/tickets", status_code=201, response_model=Tickets)
async def create_tickets_route(
    request: Request, infos: InfoPostTickets, db: AsyncSession = Depends(init_bdd)
):
    try:
        ticket: Tickets = await create_ticket(
            db, request, infos.id_order, infos.type, infos.body
        )
        await db.commit()
        return ticket

    except HTTPException as error:
        await db.rollback()
        raise HTTPException(
            status_code=error.status_code,
            detail=str(error.detail)
        ) from error


# --------------- GET ---------------
@router.get("/tickets", status_code=200, response_model=List[InfoGetTickets])
async def get_tickets_route(
    request: Request,
    id_user: str = "",
    state_flag: int = -1,
    db: AsyncSession = Depends(init_bdd),
):
    return await get_tickets(db, request, id_user, state_flag)


@router.get("/tickets/{ticket_id}", status_code=200, response_model=Tickets)
async def get_ticket_route(
    request: Request, ticket_id: str, db: AsyncSession = Depends(init_bdd)
):
    return await get_ticket(db, request, ticket_id)


# --------------- PATCH ---------------
@router.patch("/tickets/{ticket_id}", status_code=204)
async def update_ticket_route(
    request: Request,
    ticket_id: str,
    info: InfoPatchTickets,
    db: AsyncSession = Depends(init_bdd),
):
    try:
        ticket: Tickets = await update_ticket(
            db, request, ticket_id, info.type, info.body, info.state_flag
        )
        await db.commit()
        return ticket

    except HTTPException as error:
        await db.rollback()
        raise HTTPException(
            status_code=error.status_code,
            detail=str(error.detail)
        ) from error


@router.patch("/tickets/{ticket_id}/process", status_code=204)
async def process_ticket_route(
    request: Request,
    ticket_id: str,
    infos: InfoProcessTickets,
    db: AsyncSession = Depends(init_bdd),
):
    try:
        ticket: Tickets = await process_ticket(
            db, request, ticket_id, infos.state_flag, infos.body
        )
        await db.commit()
        return ticket

    except HTTPException as error:
        await db.rollback()
        raise HTTPException(
            status_code=error.status_code,
            detail=str(error.detail)
        ) from error


# --------------- DELETE ---------------
@router.delete("/tickets/{ticket_id}", status_code=200)
async def delete_one_recording_route(
    request: Request, ticket_id: str, db: AsyncSession = Depends(init_bdd)
):
    try:
        response = await delete_ticket(db, request, ticket_id)
        await db.commit()
        return response

    except HTTPException as error:
        await db.rollback()
        raise HTTPException(
            status_code=error.status_code,
            detail=str(error.detail)
        ) from error

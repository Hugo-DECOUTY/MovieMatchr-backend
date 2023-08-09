from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from moviematchr.utils.utils import init_bdd
from moviematchr.schemas.account.get_account import GetAccountSchema
from moviematchr.schemas.tickets.info_post_tickets import InfoPostTickets
from moviematchr.controller.account.get_account import get_account
from moviematchr.controller.account.create_new_user import create_new_user

router = APIRouter()

# Routes for interacting with the API
# --------------- POST ---------------
@router.post("/account/new_user", status_code=201)
async def create_ticket_and_accept_new_user_route(
    request: Request, infos: InfoPostTickets, db: AsyncSession = Depends(init_bdd)
):
    try:
        response = await create_new_user(
            db, request, infos.id_order, infos.type, infos.body
        )
        await db.commit()
        return response

    except HTTPException as error:
        await db.rollback()
        raise HTTPException(
            status_code=error.status_code, detail=str(error.detail)
        ) from error


# --------------- GET ---------------
@router.get("/account/{account_id}", status_code=200, response_model=GetAccountSchema)
async def get_account_route(request: Request, account_id: str):
    return await get_account(request, account_id)


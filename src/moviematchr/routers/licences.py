from typing import Sequence
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from moviematchr.utils.utils import init_bdd
from moviematchr.schemas.licences.licences import Licences
from moviematchr.controller.licences.get_licences_from_order import (
    get_licences_from_order,
)
from moviematchr.controller.licences.patch_user_licence import patch_user_licence

router = APIRouter()

# Routes for interacting with the API
# --------------- GET ---------------
@router.get("/licences/{id_order}", status_code=200, response_model=Sequence[Licences])
async def get_licences_from_order_route(
    request: Request, id_order: str, db: AsyncSession = Depends(init_bdd)
):
    return await get_licences_from_order(db, request, id_order)


# --------------- PATCH ---------------
@router.patch("/licences/{id_licence}/user", status_code=204)
async def patch_user_licence_route(
    request: Request, id_licence: str, db: AsyncSession = Depends(init_bdd)
):
    try:
        licence: Licences = await patch_user_licence(db, request, id_licence)
        await db.commit()
        return licence

    except HTTPException as error:
        await db.rollback()
        raise HTTPException(
            status_code=error.status_code,
            detail=str(error.detail)
        ) from error

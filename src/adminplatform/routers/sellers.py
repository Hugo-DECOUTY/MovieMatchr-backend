from typing import Sequence
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from adminplatform.utils.utils import init_bdd
from adminplatform.schemas.sellers.sellers import Sellers
from adminplatform.controller.sellers.get_sellers import get_sellers
from adminplatform.controller.sellers.get_seller import get_seller

router = APIRouter()

# Routes for interacting with the API
# --------------- GET ---------------
@router.get("/sellers", status_code=200, response_model=Sequence[Sellers])
async def get_sellers_route(
    request: Request,
    db: AsyncSession = Depends(init_bdd)):
    return await get_sellers(db, request)

@router.get("/sellers/{seller_id}", status_code=200, response_model=Sellers)
async def get_order_route(
    request: Request, seller_id: str, db: AsyncSession = Depends(init_bdd)
):
    return await get_seller(db, request, seller_id)

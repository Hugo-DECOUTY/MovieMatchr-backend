from typing import List
from fastapi import APIRouter, Depends, Request, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from moviematchr.utils.utils import init_bdd
from moviematchr.schemas.orders.orders import Orders
from moviematchr.controller.orders.create_order import create_order
from moviematchr.controller.orders.create_order_attachement import (
    create_order_attachement,
)
from moviematchr.controller.orders.get_orders import get_orders
from moviematchr.controller.orders.get_order import get_order
from moviematchr.controller.orders.get_users_from_order import get_users_from_order
from moviematchr.controller.orders.get_order_about import get_order_about
from moviematchr.controller.orders.get_order_attachement import get_order_attachement
from moviematchr.controller.orders.update_order import update_order
from moviematchr.controller.orders.update_order_billing_type import (
    update_order_billing_type,
)
from moviematchr.controller.orders.update_order_sharing_authorization import (
    update_order_sharing_authorization,
)
from moviematchr.controller.orders.update_order_demo_flag import (
    update_order_demo_flag,
)
from moviematchr.controller.orders.delete_order import delete_order

from moviematchr.schemas.orders.info_post_orders import InfoPostOrders
from moviematchr.schemas.orders.info_patch_orders import InfoPatchOrders
from moviematchr.schemas.orders.info_patch_billing_type import InfoPatchBillingType
from moviematchr.schemas.orders.info_patch_sharing_authorization import (
    InfoPatchSharingAuthorization,
)
from moviematchr.schemas.orders.info_patch_demo_flag import InfoPatchDemoFlag
from moviematchr.schemas.orders.info_get_order_informations import (
    InfoGetOrderInformations,
)

router = APIRouter()

# Routes for interacting with the API
# --------------- POST ---------------
@router.post("/orders", status_code=201, response_model=Orders)
async def create_orders_route(
    request: Request, infos: InfoPostOrders, db: AsyncSession = Depends(init_bdd)
):
    try:
        order: Orders = await create_order(db, request, infos)
        await db.commit()
        return order

    except HTTPException as error:
        await db.rollback()
        raise HTTPException(
            status_code=error.status_code,
            detail=str(error.detail)
        ) from error


@router.post("/orders/{order_id}/upload", status_code=201, response_model=bytes)
async def create_order_attachement_route(
    request: Request,
    order_id: str,
    db: AsyncSession = Depends(init_bdd),
    file: UploadFile = File(...),
):
    return await create_order_attachement(db, request, order_id, file)


# --------------- GET ---------------
@router.get("/orders", status_code=200, response_model=List[Orders])
async def get_orders_route(
    request: Request, state_flag: int = -1, db: AsyncSession = Depends(init_bdd)
):
    return await get_orders(db, request, state_flag)


@router.get("/orders/{order_id}", status_code=200, response_model=Orders)
async def get_order_route(
    request: Request, order_id: str, db: AsyncSession = Depends(init_bdd)
):
    return await get_order(db, request, order_id)


@router.get("/orders/{order_id}/users", status_code=200, response_model=List[dict])
async def get_order_users_route(
    request: Request, order_id: str, db: AsyncSession = Depends(init_bdd)
):
    return await get_users_from_order(db, request, order_id)


@router.get("/orders/{order_id}/about", status_code=200, response_model=InfoGetOrderInformations)
async def get_order_about_route(
    request: Request, order_id: str, db: AsyncSession = Depends(init_bdd)
):
    return await get_order_about(db, request, order_id)


@router.get("/orders/{order_id}/attachement", status_code=200, response_model=bytes)
async def get_order_attachement_route(
    request: Request, order_id: str, db: AsyncSession = Depends(init_bdd)
):
    return await get_order_attachement(db, request, order_id)


# --------------- PATCH ---------------
@router.patch("/orders/{order_id}", status_code=204)
async def update_order_route(
    request: Request,
    order_id: str,
    infos: InfoPatchOrders,
    db: AsyncSession = Depends(init_bdd),
):
    try:
        order: Orders = await update_order(db, request, order_id, infos)
        await db.commit()
        return order

    except HTTPException as error:
        await db.rollback()
        raise HTTPException(
            status_code=error.status_code,
            detail=str(error.detail)
        ) from error


@router.patch("/orders/type/{order_id}", status_code=204)
async def update_order_billing_type_route(
    request: Request,
    order_id: str,
    infos: InfoPatchBillingType,
    db: AsyncSession = Depends(init_bdd),
):
    try:
        response: dict = await update_order_billing_type(
            db, request, order_id, infos.billing_type
        )
        await db.commit()
        return response

    except HTTPException as error:
        await db.rollback()
        raise HTTPException(
            status_code=error.status_code,
            detail=str(error.detail)
        ) from error


@router.patch("/orders/sharing_authorization/{order_id}", status_code=204)
async def update_order_sharing_authorization_route(
    request: Request,
    order_id: str,
    infos: InfoPatchSharingAuthorization,
    db: AsyncSession = Depends(init_bdd),
):
    try:
        response: dict = await update_order_sharing_authorization(
            db, request, order_id, infos.sharing_authorization
        )
        await db.commit()
        return response

    except HTTPException as error:
        await db.rollback()
        raise HTTPException(
            status_code=error.status_code,
            detail=str(error.detail)
        ) from error
    

@router.patch("/orders/demo_flag/{order_id}", status_code=204)
async def update_order_demo_flag_route(
    request: Request,
    order_id: str,
    infos: InfoPatchDemoFlag,
    db: AsyncSession = Depends(init_bdd),
):
    try:
        response: dict = await update_order_demo_flag(
            db, request, order_id, infos.demo_flag
        )
        await db.commit()
        return response

    except HTTPException as error:
        await db.rollback()
        raise HTTPException(
            status_code=error.status_code,
            detail=str(error.detail)
        ) from error


# --------------- DELETE ---------------
@router.delete("/orders/{order_id}", status_code=200)
async def delete_order_route(
    request: Request, order_id: str, db: AsyncSession = Depends(init_bdd)
):
    try:
        await delete_order(db, request, order_id)
        await db.commit()

    except HTTPException as error:
        await db.rollback()
        raise HTTPException(
            status_code=error.status_code,
            detail=str(error.detail)
        ) from error

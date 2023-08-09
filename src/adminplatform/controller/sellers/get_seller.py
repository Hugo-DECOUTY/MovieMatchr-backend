from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from adminplatform.enum.errors.HttpErrorsEnum import HttpErrorsEnum

from adminplatform.schemas.sellers.sellers import Sellers

from adminplatform.services.sellers import get_seller_dal

from adminplatform.utils.user_group import UserGroup, get_payload_and_groups


async def get_seller(db: AsyncSession, request: Request, seller_id: str) -> Sellers:
    _, group = get_payload_and_groups(request.headers.get("X-USERINFO"))

    if group == UserGroup.HDS_ADMIN_MICROPORT.value:

        seller: Sellers = await get_seller_dal(db, seller_id)

        if seller is None:
            raise HTTPException(status_code=404, detail=HttpErrorsEnum.SELLER_NOT_FOUND.value)

        return seller

    raise HTTPException(status_code=403)

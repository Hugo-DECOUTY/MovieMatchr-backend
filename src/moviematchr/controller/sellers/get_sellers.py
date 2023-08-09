from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Sequence

from moviematchr.schemas.sellers.sellers import Sellers
from moviematchr.services.sellers import get_sellers_dal
from moviematchr.utils.user_group import UserGroup, get_payload_and_groups


async def get_sellers(db: AsyncSession, request: Request) -> Sequence[Sellers]:
    _, group = get_payload_and_groups(request.headers.get("X-USERINFO"))

    if group == UserGroup.HDS_ADMIN_MICROPORT.value:

        sellers: Sequence[Sellers] = await get_sellers_dal(db)

        return sellers

    raise HTTPException(status_code=403)

from typing import Optional
from fastapi import HTTPException, Request, File, UploadFile, Response
from sqlalchemy.ext.asyncio import AsyncSession

from moviematchr.enum.errors.HttpErrorsEnum import HttpErrorsEnum

from moviematchr.schemas.orders.orders import Orders

from moviematchr.services.orders import get_order_dal
from moviematchr.services.data_storage.post_a_upload_file_in_storage import (
    post_a_upload_file_in_storage,
)

from moviematchr.utils.user_group import UserGroup, get_payload_and_groups


async def create_order_attachement(
    db: AsyncSession,
    request: Request,
    order_id: str,
    file: Optional[UploadFile] = File(None),
):
    _, group = get_payload_and_groups(request.headers.get("X-USERINFO"))

    if group == UserGroup.HDS_ADMIN_MICROPORT.value:
        if file is None:
            raise HTTPException(status_code=400)

        order: Orders = await get_order_dal(db, order_id)

        if order is None:
            raise HTTPException(
                status_code=404, detail=HttpErrorsEnum.ORDER_NOT_FOUND.value
            )

        response: bool = post_a_upload_file_in_storage(
            file, f"{order.id}/{order.order_id}.xlsx"
        )

        if response is False:
            raise HTTPException(
                status_code=500, detail=HttpErrorsEnum.ERROR_WHILE_UPLOADING_FILE.value
            )

        return {"message": "File uploaded successfully"}

    raise HTTPException(status_code=403)

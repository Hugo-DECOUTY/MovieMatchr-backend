from pydantic import BaseModel


class InfoPatchOrders(BaseModel):
    order_id: str
    workplace: str
    service: str
    seller_id: str
    state_flag: int

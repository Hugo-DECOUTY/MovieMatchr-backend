from uuid import UUID
from pydantic import BaseModel


class InfoGetTickets(BaseModel):
    id: str
    id_order: str
    order_id: str
    workplace: str
    service: str
    user: str
    type: int = 0
    sending_date: int
    body: dict
    state_flag: int
    update_state_date: int = None

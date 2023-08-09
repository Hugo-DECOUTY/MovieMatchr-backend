from pydantic import BaseModel


class InfoProcessTickets(BaseModel):
    state_flag: int
    body: str = None

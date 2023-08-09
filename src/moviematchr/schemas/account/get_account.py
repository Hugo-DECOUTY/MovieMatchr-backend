from typing import NewType
from pydantic import BaseModel


class GetAccount(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str


GetAccountSchema = NewType("GetAccountSchema", GetAccount)

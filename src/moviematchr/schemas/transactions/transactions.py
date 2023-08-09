from enum import Enum
from pydantic import BaseModel

class TypeOfActionEnum(Enum):
    TRANSFERT = 0
    UPLOAD = 1
    SHARE = 2

class Transactions(BaseModel):
    id: str
    recording_id: str
    type_of_action: int
    date_of_action: int
    licence_id_action: str
    complementary_id: str
    email_action: str
    email_complementary: str

    class Config:
        orm_mode = True

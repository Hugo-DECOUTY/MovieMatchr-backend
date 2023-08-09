from enum import Enum
from pydantic import BaseModel

class StateOrderEnum(Enum):
    ACCEPTED = 0
    EXPIRED = 1
    ALL = 2
    DELETED = 3

class BillingTypeEnum(Enum):
    SIZE_1_TO_190 = 0
    SIZE_191_TO_385 = 1
    SIZE_386_TO_580 = 2
    SIZE_581_TO_770 = 3
    SIZE_771_TO_1150 = 4
    SIZE_1151_TO_1730 = 5

class Orders(BaseModel):
    id: str
    order_id: str
    local_admin_id: str
    nb_shared_tokens: int = 0
    billing_type: int = None
    country: str = None
    workplace: str
    service: str
    seller_id: str
    state_flag: int
    sending_date: int
    order_accepted_date: int = None
    demo_flag: bool
    sharing_authorization: bool = True
    company_only: bool = False

    class Config:
        orm_mode = True

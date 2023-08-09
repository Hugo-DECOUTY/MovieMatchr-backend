from enum import Enum

from pydantic import BaseModel, validator
from adminplatform.utils.params_validation import test_email


class TypeTicketEnum(Enum):
    MODIFY_USER = 0
    ADD_NON_MEDICAL_PERSONEL = 1
    ADD_NEW_LICENCES = 2


class StateTicketEnum(Enum):
    IN_PROGRESS = 0
    CANCELED = 1
    ACCEPTED = 2
    DENIED = 3


class TicketBody(BaseModel):
    id: str = None
    type_2fa: int = None
    email: str
    new_email: str = None
    firstname: str
    lastname: str
    serial_number: str = None
    licence_type: int = None

    @validator("new_email")
    # pylint: disable=no-self-argument
    def new_email_must_be_valid(cls, v):
        if v is not None and test_email(v) is False:
            raise ValueError("Invalid email")
        return v

class Tickets(BaseModel):
    id: str
    id_order: str
    user: str
    type: int = 0
    sending_date: int
    body: TicketBody
    state_flag: int = StateTicketEnum.IN_PROGRESS.value
    update_state_date: int = None

    class Config:
        orm_mode = True

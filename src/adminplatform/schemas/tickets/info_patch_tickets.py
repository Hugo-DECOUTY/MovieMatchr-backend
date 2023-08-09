from pydantic import BaseModel, validator
from adminplatform.schemas.tickets.tickets import TypeTicketEnum, StateTicketEnum


class InfoPatchTickets(BaseModel):
    type: int
    body: dict
    state_flag: int

    @validator("type")
    # pylint: disable=no-self-argument
    def type_must_be_valid(cls, v):
        if v not in (TypeTicketEnum.ADD_NEW_LICENCES.value, TypeTicketEnum.ADD_NON_MEDICAL_PERSONEL.value, TypeTicketEnum.MODIFY_USER.value):
            raise ValueError("Invalid type")
        return v
    
    @validator("state_flag")
    # pylint: disable=no-self-argument
    def state_flag_must_be_valid(cls, v):
        if v not in (StateTicketEnum.IN_PROGRESS.value, StateTicketEnum.ACCEPTED.value, StateTicketEnum.DENIED.value, StateTicketEnum.CANCELED.value):
            raise ValueError("Invalid state flag")
        return v

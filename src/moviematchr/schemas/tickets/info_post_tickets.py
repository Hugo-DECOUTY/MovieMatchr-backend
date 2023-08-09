from pydantic import BaseModel, validator
from moviematchr.utils.params_validation import is_valid_uuid
from moviematchr.schemas.tickets.tickets import TypeTicketEnum



class InfoPostTickets(BaseModel):
    id_order: str
    type: int
    body: dict

    @validator("id_order")
    # pylint: disable=no-self-argument
    def id_order_must_be_valid(cls, v):
        if is_valid_uuid(v) is False:
            raise ValueError("Invalid order id")
        return v
    
    @validator("type")
    # pylint: disable=no-self-argument
    def type_must_be_valid(cls, v):
        if v not in (TypeTicketEnum.ADD_NEW_LICENCES.value, TypeTicketEnum.ADD_NON_MEDICAL_PERSONEL.value, TypeTicketEnum.MODIFY_USER.value):
            raise ValueError("Invalid type")
        return v

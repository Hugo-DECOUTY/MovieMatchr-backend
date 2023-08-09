from pydantic import BaseModel


class InfoGetOrderInformations(BaseModel):
    local_admin: dict
    users: list
    seller: dict
    sum_of_recording_analyzed_in_order: int

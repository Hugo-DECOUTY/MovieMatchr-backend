from pydantic import BaseModel


class InfoGetFromStateFlag(BaseModel):
    state_flag: int

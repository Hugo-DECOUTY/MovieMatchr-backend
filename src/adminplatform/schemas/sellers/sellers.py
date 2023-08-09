from pydantic import BaseModel

class Sellers(BaseModel):
    id: str
    email: str
    firstname: str
    lastname: str
    phone: str = None


    class Config:
        orm_mode = True

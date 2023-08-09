from enum import Enum
from pydantic import BaseModel

class TypeLicenceEnum(Enum):
    DOCTOR = 0
    MEDICAL_STAFF = 1
    NON_MEDICAL_STAFF = 2
    HDS_LOCAL_ADMIN = 3
    MICROPORT_STAFF = 4

class Licences(BaseModel):
    id: str
    licence_type: int = None
    serial_number: str
    id_order: str = None
    id_user: str = None
    nb_recording_analyzed: int = 0
    demo_flag: bool
    active: bool = True

    class Config:
        orm_mode = True

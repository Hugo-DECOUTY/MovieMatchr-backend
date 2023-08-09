import uuid
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER, BOOLEAN

from moviematchr.init_base import Base


class DBLicences(Base):
    __tablename__ = "licences"

    id = Column(VARCHAR(36), primary_key=True, index=True, default=str(uuid.uuid4))
    serial_number = Column(VARCHAR(10), nullable=False, primary_key=True)
    licence_type = Column(INTEGER, nullable=True)
    id_order = Column(VARCHAR(36), ForeignKey("orders.id"), nullable=True)
    id_user = Column(VARCHAR(36), nullable=True)
    nb_recording_analyzed = Column(INTEGER, nullable=False, default=0)
    demo_flag = Column(BOOLEAN, nullable=False)
    active = Column(BOOLEAN, nullable=False, default=True)

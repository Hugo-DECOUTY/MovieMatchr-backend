import uuid
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER, JSON

from moviematchr.init_base import Base


class DBTickets(Base):
    __tablename__ = "tickets"

    id = Column(VARCHAR(36), primary_key=True, index=True, default=str(uuid.uuid4))
    id_order = Column(VARCHAR(36), ForeignKey("orders.id"))
    user = Column(VARCHAR(36), default=str(uuid.uuid4))
    type = Column(INTEGER)
    sending_date = Column(INTEGER)
    body = Column(JSON)
    state_flag = Column(INTEGER)
    update_state_date = Column(INTEGER, nullable=True)

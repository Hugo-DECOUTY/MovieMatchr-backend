import uuid
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER, BOOLEAN

from moviematchr.init_base import Base


class DBOrders(Base):
    __tablename__ = "orders"

    id = Column(VARCHAR(36), primary_key=True, index=True, default=str(uuid.uuid4))
    order_id = Column(VARCHAR(255), default="")
    local_admin_id = Column(VARCHAR(36), default=str(uuid.uuid4))
    nb_shared_tokens = Column(INTEGER, default=0)
    billing_type = Column(INTEGER, nullable=True)
    country = Column(VARCHAR(255), nullable=True)
    workplace = Column(VARCHAR(255))
    service = Column(VARCHAR(255))
    seller_id = Column(
        VARCHAR(36),
        ForeignKey("sellers.id"),
        nullable=False,
    )
    state_flag = Column(INTEGER)
    sending_date = Column(INTEGER)
    order_accepted_date = Column(INTEGER, nullable=True)
    demo_flag = Column(BOOLEAN, nullable=False)
    sharing_authorization = Column(BOOLEAN, nullable=False, default=True)
    company_only = Column(BOOLEAN, nullable=False, default=False)
